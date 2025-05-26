module miter (
  input  [  0:0] \__pi_output292.Y ,
`ifdef DIRECT_CROSS_POINTS
`else
`endif
  output [  0:0] \__po_text_out__13__gold ,
  output [  0:0] \__po_text_out__13__gate
);
  \gold.aes_cipher_top.text_out.13 gold (
    .\__pi_output292.Y (\__pi_output292.Y ),
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_text_out__13 (\__po_text_out__13__gold )
  );
  \gate.aes_cipher_top.text_out.13 gate (
    .\__pi_output292.Y (\__pi_output292.Y ),
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_text_out__13 (\__po_text_out__13__gate )
  );
`ifdef ASSUME_DEFINED_INPUTS
  miter_def_prop #(1, "assume") \__pi_output292.Y__assume (\__pi_output292.Y );
`endif
`ifndef DIRECT_CROSS_POINTS
`endif
`ifdef CHECK_MATCH_POINTS
`endif
`ifdef CHECK_OUTPUTS
  miter_cmp_prop #(1, "assert") \__po_text_out__13__assert (\__po_text_out__13__gold , \__po_text_out__13__gate );
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
  miter_def_prop #(1, "cover") \__po_text_out__13__gold_cover (\__po_text_out__13__gold );
`endif
`ifdef COVER_DEF_GATE_OUTPUTS
  miter_def_prop #(1, "cover") \__po_text_out__13__gate_cover (\__po_text_out__13__gate );
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
module \gold.aes_cipher_top.text_out.13 (
  input  [  0:0] \__pi_output292.Y ,
  output [  0:0] \__po_text_out__13
);
endmodule
module \gate.aes_cipher_top.text_out.13 (
  input  [  0:0] \__pi_output292.Y ,
  output [  0:0] \__po_text_out__13
);
endmodule
