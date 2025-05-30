// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2021-2025, The OpenROAD Authors

#include "BalancerConnection.h"

#include <dst/JobMessage.h>

#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/asio/post.hpp>
#include <boost/bind/bind.hpp>
#include <boost/serialization/export.hpp>
#include <boost/thread/thread.hpp>
#include <cstddef>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include "LoadBalancer.h"
#include "dst/BalancerJobDescription.h"
#include "dst/BroadcastJobDescription.h"
#include "dst/Distributed.h"
#include "utl/Logger.h"

using namespace dst;

BOOST_CLASS_EXPORT(dst::BalancerJobDescription)
BOOST_CLASS_EXPORT(dst::BroadcastJobDescription)

BalancerConnection::BalancerConnection(asio::io_context& service,
                                       LoadBalancer* owner,
                                       utl::Logger* logger)
    : sock_(service), logger_(logger), owner_(owner)
{
}
// socket creation
tcp::socket& BalancerConnection::socket()
{
  return sock_;
}

void BalancerConnection::start()
{
  async_read_until(
      sock_,
      in_packet_,
      JobMessage::EOP,
      [me = shared_from_this()](boost::system::error_code const& ec,
                                std::size_t bytes_xfer) {
        boost::thread t(&BalancerConnection::handle_read, me, ec, bytes_xfer);
        t.detach();
      });
}

void BalancerConnection::handle_read(boost::system::error_code const& err,
                                     size_t bytes_transferred)
{
  if (!err) {
    boost::system::error_code error;
    std::string data{buffers_begin(in_packet_.data()),
                     buffers_begin(in_packet_.data()) + bytes_transferred};
    JobMessage msg(JobMessage::NONE);
    if (!JobMessage::serializeMsg(JobMessage::READ, msg, data)) {
      logger_->warn(utl::DST,
                    42,
                    "Received malformed msg {} from port {}",
                    data,
                    sock_.remote_endpoint().port());
      asio::write(sock_, asio::buffer("0"), error);
      sock_.close();
      return;
    }
    switch (msg.getMessageType()) {
      case JobMessage::UNICAST: {
        ip::address workerAddress;
        unsigned short port;
        owner_->getNextWorker(workerAddress, port);
        if (workerAddress.is_unspecified()) {
          logger_->warn(utl::DST, 6, "No workers available");
          sock_.close();
        } else {
          if (msg.getJobType() == JobMessage::BALANCER) {
            JobMessage reply(JobMessage::SUCCESS);
            auto uDesc = std::make_unique<BalancerJobDescription>();
            auto desc = uDesc.get();
            desc->setWorkerIP(workerAddress.to_string());
            desc->setWorkerPort(port);
            reply.setJobDescription(std::move(uDesc));
            owner_->dist_->sendResult(reply, sock_);
            sock_.close();
          } else {
            asio::io_context service;
            tcp::socket socket(service);
            int failed_workers_trials = 0;
            asio::streambuf receive_buffer;
            bool failure = true;
            while (failure) {
              try {
                socket.connect(tcp::endpoint(workerAddress, port));
                asio::write(socket, in_packet_);
                asio::read(socket, receive_buffer, asio::transfer_all());
                failure = false;
              } catch (std::exception const& ex) {
                if (socket.is_open()) {
                  socket.close();
                }
                if (std::string(ex.what()).find("read: End of file")
                    != std::string::npos) {
                  // Since asio::transfer_all() used with a stream buffer it
                  // always reach an eof file exception!
                  failure = false;
                  break;
                }
                logger_->warn(utl::DST,
                              204,
                              "Exception thrown: {}. worker with ip \"{}\" and "
                              "port \"{}\" will be pushed back the queue.",
                              ex.what(),
                              workerAddress,
                              port);
                owner_->punishWorker(workerAddress, port);
                failed_workers_trials++;
                if (failed_workers_trials == MAX_FAILED_WORKERS_TRIALS) {
                  logger_->warn(utl::DST,
                                205,
                                "Maximum of {} failing workers reached, "
                                "relaying error to leader.",
                                failed_workers_trials);
                  break;
                }
                owner_->getNextWorker(workerAddress, port);
              }
            }
            if (failure) {
              JobMessage result(JobMessage::ERROR);
              std::string msgStr;
              JobMessage::serializeMsg(JobMessage::WRITE, result, msgStr);
              asio::write(sock_, asio::buffer(msgStr), error);
            } else {
              asio::write(sock_, receive_buffer, error);
            }
            sock_.close();
          }
        }
        break;
      }
      case JobMessage::BROADCAST: {
        std::lock_guard<std::mutex> lock(owner_->workers_mutex_);
        owner_->broadcastData.push_back(data);
        asio::thread_pool pool(owner_->workers_.size());
        auto workers_copy = owner_->workers_;
        std::mutex broadcast_failure_mutex;
        std::vector<std::pair<ip::address, unsigned short>> failed_workers;
        while (!workers_copy.empty()) {
          auto worker = workers_copy.top();
          workers_copy.pop();
          asio::post(
              pool,
              [worker, data, &failed_workers, &broadcast_failure_mutex]() {
                try {
                  asio::io_context service;
                  tcp::socket socket(service);
                  socket.connect(tcp::endpoint(worker.ip, worker.port));
                  asio::write(socket, asio::buffer(data));
                  asio::streambuf receive_buffer;
                  asio::read(socket, receive_buffer, asio::transfer_all());
                } catch (std::exception const& ex) {
                  if (std::string(ex.what()).find("read: End of file")
                      == std::string::npos) {
                    // Since asio::transfer_all() used with a stream buffer it
                    // always reach an eof file exception!
                    std::lock_guard<std::mutex> lock(broadcast_failure_mutex);
                    failed_workers.emplace_back(worker.ip, worker.port);
                  }
                }
              });
        }
        pool.join();
        JobMessage result(JobMessage::SUCCESS);
        std::string msgStr;
        unsigned short successBroadcast
            = owner_->workers_.size() - failed_workers.size();
        if (!failed_workers.empty()) {
          for (const auto& worker : failed_workers) {
            owner_->removeWorker(worker.first, worker.second, false);
          }
          logger_->warn(utl::DST,
                        207,
                        "{} workers failed to receive the broadcast message "
                        "and have been removed.",
                        failed_workers.size());
          if (failed_workers.size() > MAX_BROADCAST_FAILED_NODES
              || failed_workers.size() == owner_->workers_.size()) {
            result.setJobType(JobMessage::JobType::ERROR);
          }
        }
        auto uDesc = std::make_unique<BroadcastJobDescription>();
        auto desc = uDesc.get();
        desc->setWorkersCount(successBroadcast);
        result.setJobDescription(std::move(uDesc));
        JobMessage::serializeMsg(JobMessage::WRITE, result, msgStr);
        asio::write(sock_, asio::buffer(msgStr), error);
        sock_.close();
        break;
      }
    }

  } else {
    logger_->warn(utl::DST,
                  8,
                  "Balancer conhandler failed with message: {}",
                  err.message());
    sock_.close();
  }
}

#if !SWIG && FMT_VERSION >= 100000
namespace boost::asio::ip {

static auto format_as(const boost::asio::ip::address& f)
{
  return fmt::streamed(f);
}

}  // namespace boost::asio::ip
#endif
