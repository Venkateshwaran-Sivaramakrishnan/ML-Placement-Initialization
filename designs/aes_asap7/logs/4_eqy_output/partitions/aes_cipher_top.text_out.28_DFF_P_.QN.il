# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.text_out.28_DFF_P_.QN
  wire \_30786_.A
  attribute \keep 1
  wire output 1 \__po_text_out[28]$_DFF_P_.QN
  attribute \keep 1
  wire \text_out[28]$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$24706
    connect \A \_30786_.A
    connect \Y \text_out[28]$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$25231
    connect \A 1'x
    connect \Y \_30786_.A
  end
  connect \__po_text_out[28]$_DFF_P_.QN \text_out[28]$_DFF_P_.QN
end
module \gold.aes_cipher_top.text_out.28_DFF_P_.QN
  wire \_30786_.A
  attribute \keep 1
  wire output 1 \__po_text_out[28]$_DFF_P_.QN
  attribute \keep 1
  wire \text_out[28]$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$21481
    connect \A \_30786_.A
    connect \Y \text_out[28]$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$22006
    connect \A 1'x
    connect \Y \_30786_.A
  end
  connect \__po_text_out[28]$_DFF_P_.QN \text_out[28]$_DFF_P_.QN
end
