# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.output296.Y
  attribute \keep 1
  wire input 1 \__pi_output296.A
  attribute \keep 1
  wire output 2 \__po_output296.Y
  attribute \keep 1
  wire \output296.A
  attribute \keep 1
  wire \output296.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23994
    connect \A \output296.A
    connect \Y \output296.Y
  end
  connect \output296.A \__pi_output296.A
  connect \__po_output296.Y \output296.Y
end
module \gold.aes_cipher_top.output296.Y
  attribute \keep 1
  wire input 1 \__pi_output296.A
  attribute \keep 1
  wire output 2 \__po_output296.Y
  attribute \keep 1
  wire \output296.A
  attribute \keep 1
  wire \output296.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20769
    connect \A \output296.A
    connect \Y \output296.Y
  end
  connect \output296.A \__pi_output296.A
  connect \__po_output296.Y \output296.Y
end
