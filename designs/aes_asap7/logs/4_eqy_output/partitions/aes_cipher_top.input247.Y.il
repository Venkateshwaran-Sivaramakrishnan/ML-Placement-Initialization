# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input247.Y
  attribute \keep 1
  wire input 1 \__pi_input247.A
  attribute \keep 1
  wire output 2 \__po_input247.Y
  attribute \keep 1
  wire \input247.A
  attribute \keep 1
  wire \input247.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23343
    connect \A \input247.A
    connect \Y \input247.Y
  end
  connect \input247.A \__pi_input247.A
  connect \__po_input247.Y \input247.Y
end
module \gold.aes_cipher_top.input247.Y
  attribute \keep 1
  wire input 1 \__pi_input247.A
  attribute \keep 1
  wire output 2 \__po_input247.Y
  attribute \keep 1
  wire \input247.A
  attribute \keep 1
  wire \input247.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20118
    connect \A \input247.A
    connect \Y \input247.Y
  end
  connect \input247.A \__pi_input247.A
  connect \__po_input247.Y \input247.Y
end
