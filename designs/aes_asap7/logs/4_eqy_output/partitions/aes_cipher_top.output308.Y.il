# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.output308.Y
  attribute \keep 1
  wire input 1 \__pi_output308.A
  attribute \keep 1
  wire output 2 \__po_output308.Y
  attribute \keep 1
  wire \output308.A
  attribute \keep 1
  wire \output308.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$24018
    connect \A \output308.A
    connect \Y \output308.Y
  end
  connect \output308.A \__pi_output308.A
  connect \__po_output308.Y \output308.Y
end
module \gold.aes_cipher_top.output308.Y
  attribute \keep 1
  wire input 1 \__pi_output308.A
  attribute \keep 1
  wire output 2 \__po_output308.Y
  attribute \keep 1
  wire \output308.A
  attribute \keep 1
  wire \output308.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$20793
    connect \A \output308.A
    connect \Y \output308.Y
  end
  connect \output308.A \__pi_output308.A
  connect \__po_output308.Y \output308.Y
end
