# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input78.Y
  attribute \keep 1
  wire input 1 \__pi_input78.A
  attribute \keep 1
  wire output 2 \__po_input78.Y
  attribute \keep 1
  wire \input78.A
  attribute \keep 1
  wire \input78.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23483
    connect \A \input78.A
    connect \Y \input78.Y
  end
  connect \input78.A \__pi_input78.A
  connect \__po_input78.Y \input78.Y
end
module \gold.aes_cipher_top.input78.Y
  attribute \keep 1
  wire input 1 \__pi_input78.A
  attribute \keep 1
  wire output 2 \__po_input78.Y
  attribute \keep 1
  wire \input78.A
  attribute \keep 1
  wire \input78.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20258
    connect \A \input78.A
    connect \Y \input78.Y
  end
  connect \input78.A \__pi_input78.A
  connect \__po_input78.Y \input78.Y
end
