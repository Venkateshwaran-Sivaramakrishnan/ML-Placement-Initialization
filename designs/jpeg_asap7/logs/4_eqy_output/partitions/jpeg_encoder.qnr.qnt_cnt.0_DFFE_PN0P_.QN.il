# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.QN
  wire \_062925_.A
  wire \_098520_.C
  wire \_098529_.A
  wire \_110064_.A__bar
  attribute \keep 1
  wire output 1 \__po_qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$76021
    connect \A \_062925_.A
    connect \Y \_098520_.C
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$76028
    connect \A \_098520_.C
    connect \Y \_098529_.A
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$76272
    connect \A \_098529_.A
    connect \Y \_110064_.A__bar
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$81347
    connect \A \_110064_.A__bar
    connect \Y \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$81761
    connect \A 1'x
    connect \Y \_062925_.A
  end
  connect \__po_qnr.qnt_cnt[0]$_DFFE_PN0P_.QN \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
end
module \gold.jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.QN
  wire \_062925_.A
  wire \_098520_.C
  wire \_098529_.A
  wire \_110064_.A__bar
  attribute \keep 1
  wire output 1 \__po_qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  attribute \keep 1
  wire \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$64106
    connect \A \_062925_.A
    connect \Y \_098520_.C
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$64113
    connect \A \_098520_.C
    connect \Y \_098529_.A
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$64357
    connect \A \_098529_.A
    connect \Y \_110064_.A__bar
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$69432
    connect \A \_110064_.A__bar
    connect \Y \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$69846
    connect \A 1'x
    connect \Y \_062925_.A
  end
  connect \__po_qnr.qnt_cnt[0]$_DFFE_PN0P_.QN \qnr.qnt_cnt[0]$_DFFE_PN0P_.QN
end
