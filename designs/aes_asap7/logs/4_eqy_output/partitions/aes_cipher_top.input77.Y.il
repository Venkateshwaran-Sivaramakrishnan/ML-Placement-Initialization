# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input77.Y
  attribute \keep 1
  wire input 1 \__pi_input77.A
  attribute \keep 1
  wire output 2 \__po_input77.Y
  attribute \keep 1
  wire \input77.A
  attribute \keep 1
  wire \input77.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23481
    connect \A \input77.A
    connect \Y \input77.Y
  end
  connect \input77.A \__pi_input77.A
  connect \__po_input77.Y \input77.Y
end
module \gold.aes_cipher_top.input77.Y
  attribute \keep 1
  wire input 1 \__pi_input77.A
  attribute \keep 1
  wire output 2 \__po_input77.Y
  attribute \keep 1
  wire \input77.A
  attribute \keep 1
  wire \input77.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20256
    connect \A \input77.A
    connect \Y \input77.Y
  end
  connect \input77.A \__pi_input77.A
  connect \__po_input77.Y \input77.Y
end
