# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.output382.A
  wire \_30860_.Y
  attribute \keep 1
  wire input 1 \__pi_text_out[95]$_DFF_P_.int_fwire_IQN
  attribute \keep 1
  wire output 2 \__po_output382.A
  wire \net448
  attribute \keep 1
  wire \output382.A
  attribute \keep 1
  wire \text_out[95]$_DFF_P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$23883
    connect \A \_30860_.Y
    connect \Y \net448
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$24165
    connect \A \net448
    connect \Y \output382.A
  end
  cell $not $flatten\_30860_.$not$/work/practice0/flow/platforms/asap7/work_around_yosys/asap7sc7p5t_INVBUF_RVT_TT_201020.v:0$1751
    parameter \A_SIGNED 0
    parameter \A_WIDTH 1
    parameter \Y_WIDTH 1
    connect \A \text_out[95]$_DFF_P_.int_fwire_IQN
    connect \Y \_30860_.Y
  end
  connect \text_out[95]$_DFF_P_.int_fwire_IQN \__pi_text_out[95]$_DFF_P_.int_fwire_IQN
  connect \__po_output382.A \output382.A
end
module \gold.aes_cipher_top.output382.A
  wire \_30860_.Y
  attribute \keep 1
  wire input 1 \__pi_text_out[95]$_DFF_P_.int_fwire_IQN
  attribute \keep 1
  wire output 2 \__po_output382.A
  wire \net448
  attribute \keep 1
  wire \output382.A
  attribute \keep 1
  wire \text_out[95]$_DFF_P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$20658
    connect \A \_30860_.Y
    connect \Y \net448
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$20940
    connect \A \net448
    connect \Y \output382.A
  end
  cell $not $flatten\_30860_.$not$/work/practice0/flow/platforms/asap7/work_around_yosys/asap7sc7p5t_INVBUF_RVT_TT_201020.v:0$1751
    parameter \A_SIGNED 0
    parameter \A_WIDTH 1
    parameter \Y_WIDTH 1
    connect \A \text_out[95]$_DFF_P_.int_fwire_IQN
    connect \Y \_30860_.Y
  end
  connect \text_out[95]$_DFF_P_.int_fwire_IQN \__pi_text_out[95]$_DFF_P_.int_fwire_IQN
  connect \__po_output382.A \output382.A
end
