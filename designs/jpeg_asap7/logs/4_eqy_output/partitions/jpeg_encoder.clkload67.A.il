# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload67.A
  attribute \keep 1
  wire input 1 \__pi_clkload66.A
  attribute \keep 1
  wire output 2 \__po_clkload67.A
  attribute \keep 1
  wire \clkload66.A
  attribute \keep 1
  wire \clkload67.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76631
    connect \A \clkload66.A
    connect \Y \clkload67.A
  end
  connect \clkload66.A \__pi_clkload66.A
  connect \__po_clkload67.A \clkload67.A
end
module \gold.jpeg_encoder.clkload67.A
  attribute \keep 1
  wire input 1 \__pi_clkload66.A
  attribute \keep 1
  wire output 2 \__po_clkload67.A
  attribute \keep 1
  wire \clkload66.A
  attribute \keep 1
  wire \clkload67.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64716
    connect \A \clkload66.A
    connect \Y \clkload67.A
  end
  connect \clkload66.A \__pi_clkload66.A
  connect \__po_clkload67.A \clkload67.A
end
