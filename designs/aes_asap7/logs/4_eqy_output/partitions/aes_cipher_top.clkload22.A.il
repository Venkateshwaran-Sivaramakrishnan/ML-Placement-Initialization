# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.clkload22.A
  attribute \keep 1
  wire input 1 \__pi_clkload21.A
  attribute \keep 1
  wire output 2 \__po_clkload22.A
  attribute \keep 1
  wire \clkload21.A
  attribute \keep 1
  wire \clkload22.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$22949
    connect \A \clkload21.A
    connect \Y \clkload22.A
  end
  connect \clkload21.A \__pi_clkload21.A
  connect \__po_clkload22.A \clkload22.A
end
module \gold.aes_cipher_top.clkload22.A
  attribute \keep 1
  wire input 1 \__pi_clkload21.A
  attribute \keep 1
  wire output 2 \__po_clkload22.A
  attribute \keep 1
  wire \clkload21.A
  attribute \keep 1
  wire \clkload22.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$19724
    connect \A \clkload21.A
    connect \Y \clkload22.A
  end
  connect \clkload21.A \__pi_clkload21.A
  connect \__po_clkload22.A \clkload22.A
end
