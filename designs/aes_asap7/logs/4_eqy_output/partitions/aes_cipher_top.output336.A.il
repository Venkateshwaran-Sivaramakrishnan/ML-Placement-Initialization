# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.output336.A
  wire \_30814_.Y
  attribute \keep 1
  wire input 1 \__pi_text_out[53]$_DFF_P_.int_fwire_IQN
  attribute \keep 1
  wire output 2 \__po_output336.A
  wire \net402
  attribute \keep 1
  wire \output336.A
  attribute \keep 1
  wire \text_out[53]$_DFF_P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$23836
    connect \A \_30814_.Y
    connect \Y \net402
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$24073
    connect \A \net402
    connect \Y \output336.A
  end
  cell $not $flatten\_30814_.$not$/work/practice0/flow/platforms/asap7/work_around_yosys/asap7sc7p5t_INVBUF_RVT_TT_201020.v:0$1750
    parameter \A_SIGNED 0
    parameter \A_WIDTH 1
    parameter \Y_WIDTH 1
    connect \A \text_out[53]$_DFF_P_.int_fwire_IQN
    connect \Y \_30814_.Y
  end
  connect \text_out[53]$_DFF_P_.int_fwire_IQN \__pi_text_out[53]$_DFF_P_.int_fwire_IQN
  connect \__po_output336.A \output336.A
end
module \gold.aes_cipher_top.output336.A
  wire \_30814_.Y
  attribute \keep 1
  wire input 1 \__pi_text_out[53]$_DFF_P_.int_fwire_IQN
  attribute \keep 1
  wire output 2 \__po_output336.A
  wire \net402
  attribute \keep 1
  wire \output336.A
  attribute \keep 1
  wire \text_out[53]$_DFF_P_.int_fwire_IQN
  cell $_BUF_ $auto$insbuf.cc:97:execute$20611
    connect \A \_30814_.Y
    connect \Y \net402
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$20848
    connect \A \net402
    connect \Y \output336.A
  end
  cell $not $flatten\_30814_.$not$/work/practice0/flow/platforms/asap7/work_around_yosys/asap7sc7p5t_INVBUF_RVT_TT_201020.v:0$1750
    parameter \A_SIGNED 0
    parameter \A_WIDTH 1
    parameter \Y_WIDTH 1
    connect \A \text_out[53]$_DFF_P_.int_fwire_IQN
    connect \Y \_30814_.Y
  end
  connect \text_out[53]$_DFF_P_.int_fwire_IQN \__pi_text_out[53]$_DFF_P_.int_fwire_IQN
  connect \__po_output336.A \output336.A
end
