# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.u0.r0.out.24_SDFF_PP1_.CLK
  attribute \keep 1
  wire input 1 \__pi_text_out[9]$_DFF_P_.CLK
  attribute \keep 1
  wire output 2 \__po_u0.r0.out[24]$_SDFF_PP1_.CLK
  attribute \keep 1
  wire \text_out[9]$_DFF_P_.CLK
  attribute \keep 1
  wire \u0.r0.out[24]$_SDFF_PP1_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$24945
    connect \A \text_out[9]$_DFF_P_.CLK
    connect \Y \u0.r0.out[24]$_SDFF_PP1_.CLK
  end
  connect \text_out[9]$_DFF_P_.CLK \__pi_text_out[9]$_DFF_P_.CLK
  connect \__po_u0.r0.out[24]$_SDFF_PP1_.CLK \u0.r0.out[24]$_SDFF_PP1_.CLK
end
module \gold.aes_cipher_top.u0.r0.out.24_SDFF_PP1_.CLK
  attribute \keep 1
  wire input 1 \__pi_text_out[9]$_DFF_P_.CLK
  attribute \keep 1
  wire output 2 \__po_u0.r0.out[24]$_SDFF_PP1_.CLK
  attribute \keep 1
  wire \text_out[9]$_DFF_P_.CLK
  attribute \keep 1
  wire \u0.r0.out[24]$_SDFF_PP1_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$21720
    connect \A \text_out[9]$_DFF_P_.CLK
    connect \Y \u0.r0.out[24]$_SDFF_PP1_.CLK
  end
  connect \text_out[9]$_DFF_P_.CLK \__pi_text_out[9]$_DFF_P_.CLK
  connect \__po_u0.r0.out[24]$_SDFF_PP1_.CLK \u0.r0.out[24]$_SDFF_PP1_.CLK
end
