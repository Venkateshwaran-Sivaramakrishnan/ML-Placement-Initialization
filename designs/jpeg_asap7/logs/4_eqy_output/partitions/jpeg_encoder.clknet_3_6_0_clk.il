# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clknet_3_6_0_clk
  attribute \keep 1
  wire input 1 \__pi_clknet_3_5_0_clk
  attribute \keep 1
  wire output 2 \__po_clknet_3_6_0_clk
  attribute \keep 1
  wire \clknet_3_5_0_clk
  attribute \keep 1
  wire \clknet_3_6_0_clk
  cell $_BUF_ $auto$insbuf.cc:97:execute$76681
    connect \A \clknet_3_5_0_clk
    connect \Y \clknet_3_6_0_clk
  end
  connect \clknet_3_5_0_clk \__pi_clknet_3_5_0_clk
  connect \__po_clknet_3_6_0_clk \clknet_3_6_0_clk
end
module \gold.jpeg_encoder.clknet_3_6_0_clk
  attribute \keep 1
  wire input 1 \__pi_clknet_3_5_0_clk
  attribute \keep 1
  wire output 2 \__po_clknet_3_6_0_clk
  attribute \keep 1
  wire \clknet_3_5_0_clk
  attribute \keep 1
  wire \clknet_3_6_0_clk
  cell $_BUF_ $auto$insbuf.cc:97:execute$64766
    connect \A \clknet_3_5_0_clk
    connect \Y \clknet_3_6_0_clk
  end
  connect \clknet_3_5_0_clk \__pi_clknet_3_5_0_clk
  connect \__po_clknet_3_6_0_clk \clknet_3_6_0_clk
end
