# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input215.Y
  attribute \keep 1
  wire input 1 \__pi_input215.A
  attribute \keep 1
  wire output 2 \__po_input215.Y
  attribute \keep 1
  wire \input215.A
  attribute \keep 1
  wire \input215.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23273
    connect \A \input215.A
    connect \Y \input215.Y
  end
  connect \input215.A \__pi_input215.A
  connect \__po_input215.Y \input215.Y
end
module \gold.aes_cipher_top.input215.Y
  attribute \keep 1
  wire input 1 \__pi_input215.A
  attribute \keep 1
  wire output 2 \__po_input215.Y
  attribute \keep 1
  wire \input215.A
  attribute \keep 1
  wire \input215.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20048
    connect \A \input215.A
    connect \Y \input215.Y
  end
  connect \input215.A \__pi_input215.A
  connect \__po_input215.Y \input215.Y
end
