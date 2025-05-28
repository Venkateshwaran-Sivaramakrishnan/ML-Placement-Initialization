module miter (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
  output [  0:0] \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gold ,
  output [  0:0] \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gate
);
  \gold.jpeg_encoder.fdct_zigzag.dct_mod.dddcnt_DFFE_PN1P_.SETN gold (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN (\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gold )
  );
  \gate.jpeg_encoder.fdct_zigzag.dct_mod.dddcnt_DFFE_PN1P_.SETN gate (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN (\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gate )
  );
`ifdef ASSUME_DEFINED_INPUTS
`endif
`ifndef DIRECT_CROSS_POINTS
`endif
`ifdef CHECK_MATCH_POINTS
`endif
`ifdef CHECK_OUTPUTS
  miter_cmp_prop #(1, "assert") \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__assert (\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gold , \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gate );
`endif
`ifdef COVER_DEF_CROSS_POINTS
  `ifdef DIRECT_CROSS_POINTS
  `else
  `endif
`endif
`ifdef COVER_DEF_GOLD_MATCH_POINTS
`endif
`ifdef COVER_DEF_GATE_MATCH_POINTS
`endif
`ifdef COVER_DEF_GOLD_OUTPUTS
  miter_def_prop #(1, "cover") \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gold_cover (\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gold );
`endif
`ifdef COVER_DEF_GATE_OUTPUTS
  miter_def_prop #(1, "cover") \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gate_cover (\__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN__gate );
`endif
endmodule
module miter_cmp_prop #(parameter WIDTH=1, parameter TYPE="assert") (input [WIDTH-1:0] in_gold, in_gate);
  reg okay;
  integer i;
  always @* begin
    okay = 1;
    for (i = 0; i < WIDTH; i = i+1)
      okay = okay && (in_gold[i] === 1'bx || in_gold[i] === in_gate[i]);
  end
  generate
    if (TYPE == "assert") always @* assert(okay);
    if (TYPE == "assume") always @* assume(okay);
    if (TYPE == "cover")  always @* cover(okay);
  endgenerate
endmodule
module miter_def_prop #(parameter WIDTH=1, parameter TYPE="assert") (input [WIDTH-1:0] in);
  wire okay = ^in !== 1'bx;
  generate
    if (TYPE == "assert") always @* assert(okay);
    if (TYPE == "assume") always @* assume(okay);
    if (TYPE == "cover")  always @* cover(okay);
  endgenerate
endmodule
module \gold.jpeg_encoder.fdct_zigzag.dct_mod.dddcnt_DFFE_PN1P_.SETN (
  output [  0:0] \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN
);
endmodule
module \gate.jpeg_encoder.fdct_zigzag.dct_mod.dddcnt_DFFE_PN1P_.SETN (
  output [  0:0] \__po_fdct_zigzag.dct_mod.dddcnt$_DFFE_PN1P_.SETN
);
endmodule
