module miter (
  input  [  0:0] \__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 ,
`ifdef DIRECT_CROSS_POINTS
`else
`endif
  output [  0:0] \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gold ,
  output [  0:0] \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gate
);
  \gold.jpeg_encoder.rle.rz1.deno_DFFE_PN0P_.SETN gold (
    .\__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 (\__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 ),
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_rle.rz1.deno$_DFFE_PN0P_.SETN (\__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gold )
  );
  \gate.jpeg_encoder.rle.rz1.deno_DFFE_PN0P_.SETN gate (
    .\__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 (\__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 ),
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_rle.rz1.deno$_DFFE_PN0P_.SETN (\__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gate )
  );
`ifdef ASSUME_DEFINED_INPUTS
  miter_def_prop #(1, "assume") \__pi_rle.rz1.den$_DFFE_PN0P_.adacond0__assume (\__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 );
`endif
`ifndef DIRECT_CROSS_POINTS
`endif
`ifdef CHECK_MATCH_POINTS
`endif
`ifdef CHECK_OUTPUTS
  miter_cmp_prop #(1, "assert") \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__assert (\__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gold , \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gate );
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
  miter_def_prop #(1, "cover") \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gold_cover (\__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gold );
`endif
`ifdef COVER_DEF_GATE_OUTPUTS
  miter_def_prop #(1, "cover") \__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gate_cover (\__po_rle.rz1.deno$_DFFE_PN0P_.SETN__gate );
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
module \gold.jpeg_encoder.rle.rz1.deno_DFFE_PN0P_.SETN (
  input  [  0:0] \__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 ,
  output [  0:0] \__po_rle.rz1.deno$_DFFE_PN0P_.SETN
);
endmodule
module \gate.jpeg_encoder.rle.rz1.deno_DFFE_PN0P_.SETN (
  input  [  0:0] \__pi_rle.rz1.den$_DFFE_PN0P_.adacond0 ,
  output [  0:0] \__po_rle.rz1.deno$_DFFE_PN0P_.SETN
);
endmodule
