# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.text_out.72_DFF_P_.QN
  wire \_30835_.A
  attribute \keep 1
  wire output 1 \__po_text_out[72]$_DFF_P_.QN
  attribute \keep 1
  wire \text_out[72]$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$24853
    connect \A \_30835_.A
    connect \Y \text_out[72]$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$25165
    connect \A 1'x
    connect \Y \_30835_.A
  end
  connect \__po_text_out[72]$_DFF_P_.QN \text_out[72]$_DFF_P_.QN
end
module \gold.aes_cipher_top.text_out.72_DFF_P_.QN
  wire \_30835_.A
  attribute \keep 1
  wire output 1 \__po_text_out[72]$_DFF_P_.QN
  attribute \keep 1
  wire \text_out[72]$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$21628
    connect \A \_30835_.A
    connect \Y \text_out[72]$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$21940
    connect \A 1'x
    connect \Y \_30835_.A
  end
  connect \__po_text_out[72]$_DFF_P_.QN \text_out[72]$_DFF_P_.QN
end
