# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.clknet_leaf_52_clk
  attribute \keep 1
  wire input 1 \__pi_clknet_leaf_51_clk
  attribute \keep 1
  wire output 2 \__po_clknet_leaf_52_clk
  attribute \keep 1
  wire \clknet_leaf_51_clk
  attribute \keep 1
  wire \clknet_leaf_52_clk
  cell $_BUF_ $auto$insbuf.cc:97:execute$76740
    connect \A \clknet_leaf_51_clk
    connect \Y \clknet_leaf_52_clk
  end
  connect \clknet_leaf_51_clk \__pi_clknet_leaf_51_clk
  connect \__po_clknet_leaf_52_clk \clknet_leaf_52_clk
end
module \gold.jpeg_encoder.clknet_leaf_52_clk
  attribute \keep 1
  wire input 1 \__pi_clknet_leaf_51_clk
  attribute \keep 1
  wire output 2 \__po_clknet_leaf_52_clk
  attribute \keep 1
  wire \clknet_leaf_51_clk
  attribute \keep 1
  wire \clknet_leaf_52_clk
  cell $_BUF_ $auto$insbuf.cc:97:execute$64825
    connect \A \clknet_leaf_51_clk
    connect \Y \clknet_leaf_52_clk
  end
  connect \clknet_leaf_51_clk \__pi_clknet_leaf_51_clk
  connect \__po_clknet_leaf_52_clk \clknet_leaf_52_clk
end
