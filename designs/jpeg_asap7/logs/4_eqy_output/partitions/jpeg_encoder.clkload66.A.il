# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload66.A
  attribute \keep 1
  wire input 1 \__pi_clkload65.A
  attribute \keep 1
  wire output 2 \__po_clkload66.A
  attribute \keep 1
  wire \clkload65.A
  attribute \keep 1
  wire \clkload66.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76630
    connect \A \clkload65.A
    connect \Y \clkload66.A
  end
  connect \clkload65.A \__pi_clkload65.A
  connect \__po_clkload66.A \clkload66.A
end
module \gold.jpeg_encoder.clkload66.A
  attribute \keep 1
  wire input 1 \__pi_clkload65.A
  attribute \keep 1
  wire output 2 \__po_clkload66.A
  attribute \keep 1
  wire \clkload65.A
  attribute \keep 1
  wire \clkload66.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64715
    connect \A \clkload65.A
    connect \Y \clkload66.A
  end
  connect \clkload65.A \__pi_clkload65.A
  connect \__po_clkload66.A \clkload66.A
end
