# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload2.A
  attribute \keep 1
  wire input 1 \__pi_clkload19.A
  attribute \keep 1
  wire output 2 \__po_clkload2.A
  attribute \keep 1
  wire \clkload19.A
  attribute \keep 1
  wire \clkload2.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76576
    connect \A \clkload19.A
    connect \Y \clkload2.A
  end
  connect \clkload19.A \__pi_clkload19.A
  connect \__po_clkload2.A \clkload2.A
end
module \gold.jpeg_encoder.clkload2.A
  attribute \keep 1
  wire input 1 \__pi_clkload19.A
  attribute \keep 1
  wire output 2 \__po_clkload2.A
  attribute \keep 1
  wire \clkload19.A
  attribute \keep 1
  wire \clkload2.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64661
    connect \A \clkload19.A
    connect \Y \clkload2.A
  end
  connect \clkload19.A \__pi_clkload19.A
  connect \__po_clkload2.A \clkload2.A
end
