# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.u0.r0.rcnt.1_SDFF_PP0_.CLK
  attribute \keep 1
  wire input 1 \__pi_u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire output 2 \__po_u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire \u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$24954
    connect \A \u0.r0.rcnt[0]$_SDFF_PP0_.CLK
    connect \Y \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  end
  connect \u0.r0.rcnt[0]$_SDFF_PP0_.CLK \__pi_u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  connect \__po_u0.r0.rcnt[1]$_SDFF_PP0_.CLK \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
end
module \gold.aes_cipher_top.u0.r0.rcnt.1_SDFF_PP0_.CLK
  attribute \keep 1
  wire input 1 \__pi_u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire output 2 \__po_u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire \u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  attribute \keep 1
  wire \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$21729
    connect \A \u0.r0.rcnt[0]$_SDFF_PP0_.CLK
    connect \Y \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
  end
  connect \u0.r0.rcnt[0]$_SDFF_PP0_.CLK \__pi_u0.r0.rcnt[0]$_SDFF_PP0_.CLK
  connect \__po_u0.r0.rcnt[1]$_SDFF_PP0_.CLK \u0.r0.rcnt[1]$_SDFF_PP0_.CLK
end
