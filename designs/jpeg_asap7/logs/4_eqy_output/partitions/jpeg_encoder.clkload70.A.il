# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload70.A
  attribute \keep 1
  wire input 1 \__pi_clkload7.Y
  attribute \keep 1
  wire output 2 \__po_clkload70.A
  attribute \keep 1
  wire \clkload7.Y
  attribute \keep 1
  wire \clkload70.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76636
    connect \A \clkload7.Y
    connect \Y \clkload70.A
  end
  connect \clkload7.Y \__pi_clkload7.Y
  connect \__po_clkload70.A \clkload70.A
end
module \gold.jpeg_encoder.clkload70.A
  attribute \keep 1
  wire input 1 \__pi_clkload7.Y
  attribute \keep 1
  wire output 2 \__po_clkload70.A
  attribute \keep 1
  wire \clkload7.Y
  attribute \keep 1
  wire \clkload70.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64721
    connect \A \clkload7.Y
    connect \Y \clkload70.A
  end
  connect \clkload7.Y \__pi_clkload7.Y
  connect \__po_clkload70.A \clkload70.A
end
