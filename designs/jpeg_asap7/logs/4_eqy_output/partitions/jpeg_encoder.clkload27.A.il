# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload27.A
  attribute \keep 1
  wire input 1 \__pi_clkload26.A
  attribute \keep 1
  wire output 2 \__po_clkload27.A
  attribute \keep 1
  wire \clkload26.A
  attribute \keep 1
  wire \clkload27.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76584
    connect \A \clkload26.A
    connect \Y \clkload27.A
  end
  connect \clkload26.A \__pi_clkload26.A
  connect \__po_clkload27.A \clkload27.A
end
module \gold.jpeg_encoder.clkload27.A
  attribute \keep 1
  wire input 1 \__pi_clkload26.A
  attribute \keep 1
  wire output 2 \__po_clkload27.A
  attribute \keep 1
  wire \clkload26.A
  attribute \keep 1
  wire \clkload27.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64669
    connect \A \clkload26.A
    connect \Y \clkload27.A
  end
  connect \clkload26.A \__pi_clkload26.A
  connect \__po_clkload27.A \clkload27.A
end
