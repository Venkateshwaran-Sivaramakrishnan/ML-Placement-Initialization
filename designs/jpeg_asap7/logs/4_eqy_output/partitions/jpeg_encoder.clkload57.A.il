# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clkload57.A
  attribute \keep 1
  wire input 1 \__pi_clkload56.A
  attribute \keep 1
  wire output 2 \__po_clkload57.A
  attribute \keep 1
  wire \clkload56.A
  attribute \keep 1
  wire \clkload57.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$76619
    connect \A \clkload56.A
    connect \Y \clkload57.A
  end
  connect \clkload56.A \__pi_clkload56.A
  connect \__po_clkload57.A \clkload57.A
end
module \gold.jpeg_encoder.clkload57.A
  attribute \keep 1
  wire input 1 \__pi_clkload56.A
  attribute \keep 1
  wire output 2 \__po_clkload57.A
  attribute \keep 1
  wire \clkload56.A
  attribute \keep 1
  wire \clkload57.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$64704
    connect \A \clkload56.A
    connect \Y \clkload57.A
  end
  connect \clkload56.A \__pi_clkload56.A
  connect \__po_clkload57.A \clkload57.A
end
