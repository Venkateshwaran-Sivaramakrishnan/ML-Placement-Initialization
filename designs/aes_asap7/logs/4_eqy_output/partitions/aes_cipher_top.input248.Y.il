# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input248.Y
  attribute \keep 1
  wire input 1 \__pi_input248.A
  attribute \keep 1
  wire output 2 \__po_input248.Y
  attribute \keep 1
  wire \input248.A
  attribute \keep 1
  wire \input248.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23345
    connect \A \input248.A
    connect \Y \input248.Y
  end
  connect \input248.A \__pi_input248.A
  connect \__po_input248.Y \input248.Y
end
module \gold.aes_cipher_top.input248.Y
  attribute \keep 1
  wire input 1 \__pi_input248.A
  attribute \keep 1
  wire output 2 \__po_input248.Y
  attribute \keep 1
  wire \input248.A
  attribute \keep 1
  wire \input248.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20120
    connect \A \input248.A
    connect \Y \input248.Y
  end
  connect \input248.A \__pi_input248.A
  connect \__po_input248.Y \input248.Y
end
