# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload99.A
  attribute \keep 1
  wire input 1 \__pi_clkload98.A
  attribute \keep 1
  wire output 2 \__po_clkload99.A
  attribute \keep 1
  wire \clkload98.A
  attribute \keep 1
  wire \clkload99.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76668
    connect \A \clkload98.A
    connect \Y \clkload99.A
  end
  connect \clkload98.A \__pi_clkload98.A
  connect \__po_clkload99.A \clkload99.A
end
module \gold.jpeg_encoder.clkload99.A
  attribute \keep 1
  wire input 1 \__pi_clkload98.A
  attribute \keep 1
  wire output 2 \__po_clkload99.A
  attribute \keep 1
  wire \clkload98.A
  attribute \keep 1
  wire \clkload99.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64753
    connect \A \clkload98.A
    connect \Y \clkload99.A
  end
  connect \clkload98.A \__pi_clkload98.A
  connect \__po_clkload99.A \clkload99.A
end
