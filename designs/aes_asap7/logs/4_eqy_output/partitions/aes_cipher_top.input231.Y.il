# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input231.Y
  attribute \keep 1
  wire input 1 \__pi_input231.A
  attribute \keep 1
  wire output 2 \__po_input231.Y
  attribute \keep 1
  wire \input231.A
  attribute \keep 1
  wire \input231.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23309
    connect \A \input231.A
    connect \Y \input231.Y
  end
  connect \input231.A \__pi_input231.A
  connect \__po_input231.Y \input231.Y
end
module \gold.aes_cipher_top.input231.Y
  attribute \keep 1
  wire input 1 \__pi_input231.A
  attribute \keep 1
  wire output 2 \__po_input231.Y
  attribute \keep 1
  wire \input231.A
  attribute \keep 1
  wire \input231.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20084
    connect \A \input231.A
    connect \Y \input231.Y
  end
  connect \input231.A \__pi_input231.A
  connect \__po_input231.Y \input231.Y
end
