# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.qnr.qnt_cnt.2_DFFE_PN0P_.int_fwire_IQN
  attribute \keep 1
  wire input 1 \__pi_qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire output 2 \__po_qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  attribute \keep 1
  wire \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$81368
    connect \A \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
    connect \Y \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  end
  connect \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN \__pi_qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  connect \__po_qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
end
module \gold.jpeg_encoder.qnr.qnt_cnt.2_DFFE_PN0P_.int_fwire_IQN
  attribute \keep 1
  wire input 1 \__pi_qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire output 2 \__po_qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  attribute \keep 1
  wire \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$69453
    connect \A \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
    connect \Y \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
  end
  connect \qnr.qnt_cnt[2]$_DFFE_PN0P_.QN \__pi_qnr.qnt_cnt[2]$_DFFE_PN0P_.QN
  connect \__po_qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN \qnr.qnt_cnt[2]$_DFFE_PN0P_.int_fwire_IQN
end
