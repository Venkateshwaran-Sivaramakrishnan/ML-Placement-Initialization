# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input257.Y
  attribute \keep 1
  wire input 1 \__pi_input257.A
  attribute \keep 1
  wire output 2 \__po_input257.Y
  attribute \keep 1
  wire \input257.A
  attribute \keep 1
  wire \input257.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23365
    connect \A \input257.A
    connect \Y \input257.Y
  end
  connect \input257.A \__pi_input257.A
  connect \__po_input257.Y \input257.Y
end
module \gold.aes_cipher_top.input257.Y
  attribute \keep 1
  wire input 1 \__pi_input257.A
  attribute \keep 1
  wire output 2 \__po_input257.Y
  attribute \keep 1
  wire \input257.A
  attribute \keep 1
  wire \input257.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20140
    connect \A \input257.A
    connect \Y \input257.Y
  end
  connect \input257.A \__pi_input257.A
  connect \__po_input257.Y \input257.Y
end
