# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input207.Y
  attribute \keep 1
  wire input 1 \__pi_input207.A
  attribute \keep 1
  wire output 2 \__po_input207.Y
  attribute \keep 1
  wire \input207.A
  attribute \keep 1
  wire \input207.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23255
    connect \A \input207.A
    connect \Y \input207.Y
  end
  connect \input207.A \__pi_input207.A
  connect \__po_input207.Y \input207.Y
end
module \gold.aes_cipher_top.input207.Y
  attribute \keep 1
  wire input 1 \__pi_input207.A
  attribute \keep 1
  wire output 2 \__po_input207.Y
  attribute \keep 1
  wire \input207.A
  attribute \keep 1
  wire \input207.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20030
    connect \A \input207.A
    connect \Y \input207.Y
  end
  connect \input207.A \__pi_input207.A
  connect \__po_input207.Y \input207.Y
end
