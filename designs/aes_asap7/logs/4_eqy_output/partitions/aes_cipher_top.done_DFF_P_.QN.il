# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.done_DFF_P_.QN
  wire \_30737_.A
  attribute \keep 1
  wire output 1 \__po_done$_DFF_P_.QN
  attribute \keep 1
  wire \done$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$23012
    connect \A \_30737_.A
    connect \Y \done$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$25185
    connect \A 1'x
    connect \Y \_30737_.A
  end
  connect \__po_done$_DFF_P_.QN \done$_DFF_P_.QN
end
module \gold.aes_cipher_top.done_DFF_P_.QN
  wire \_30737_.A
  attribute \keep 1
  wire output 1 \__po_done$_DFF_P_.QN
  attribute \keep 1
  wire \done$_DFF_P_.QN
  cell $_BUF_ $auto$insbuf.cc:97:execute$19787
    connect \A \_30737_.A
    connect \Y \done$_DFF_P_.QN
  end
  cell $_BUF_ $auto$insbuf.cc:97:execute$21960
    connect \A 1'x
    connect \Y \_30737_.A
  end
  connect \__po_done$_DFF_P_.QN \done$_DFF_P_.QN
end
