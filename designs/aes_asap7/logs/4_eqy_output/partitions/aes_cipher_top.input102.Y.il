# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input102.Y
  attribute \keep 1
  wire input 1 \__pi_input102.A
  attribute \keep 1
  wire output 2 \__po_input102.Y
  attribute \keep 1
  wire \input102.A
  attribute \keep 1
  wire \input102.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23023
    connect \A \input102.A
    connect \Y \input102.Y
  end
  connect \input102.A \__pi_input102.A
  connect \__po_input102.Y \input102.Y
end
module \gold.aes_cipher_top.input102.Y
  attribute \keep 1
  wire input 1 \__pi_input102.A
  attribute \keep 1
  wire output 2 \__po_input102.Y
  attribute \keep 1
  wire \input102.A
  attribute \keep 1
  wire \input102.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$19798
    connect \A \input102.A
    connect \Y \input102.Y
  end
  connect \input102.A \__pi_input102.A
  connect \__po_input102.Y \input102.Y
end
