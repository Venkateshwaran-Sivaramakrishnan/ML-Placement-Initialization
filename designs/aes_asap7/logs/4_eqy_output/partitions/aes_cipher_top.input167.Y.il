# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.input167.Y
  attribute \keep 1
  wire input 1 \__pi_input167.A
  attribute \keep 1
  wire output 2 \__po_input167.Y
  attribute \keep 1
  wire \input167.A
  attribute \keep 1
  wire \input167.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$23165
    connect \A \input167.A
    connect \Y \input167.Y
  end
  connect \input167.A \__pi_input167.A
  connect \__po_input167.Y \input167.Y
end
module \gold.aes_cipher_top.input167.Y
  attribute \keep 1
  wire input 1 \__pi_input167.A
  attribute \keep 1
  wire output 2 \__po_input167.Y
  attribute \keep 1
  wire \input167.A
  attribute \keep 1
  wire \input167.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$19940
    connect \A \input167.A
    connect \Y \input167.Y
  end
  connect \input167.A \__pi_input167.A
  connect \__po_input167.Y \input167.Y
end
