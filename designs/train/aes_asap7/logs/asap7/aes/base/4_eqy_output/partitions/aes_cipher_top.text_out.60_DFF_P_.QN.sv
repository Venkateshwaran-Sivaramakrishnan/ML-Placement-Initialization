module miter (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
  output [  0:0] \__po_text_out[60]$_DFF_P_.QN__gold ,
  output [  0:0] \__po_text_out[60]$_DFF_P_.QN__gate
);
  \gold.aes_cipher_top.text_out.60_DFF_P_.QN gold (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_text_out[60]$_DFF_P_.QN (\__po_text_out[60]$_DFF_P_.QN__gold )
  );
  \gate.aes_cipher_top.text_out.60_DFF_P_.QN gate (
`ifdef DIRECT_CROSS_POINTS
`else
`endif
    .\__po_text_out[60]$_DFF_P_.QN (\__po_text_out[60]$_DFF_P_.QN__gate )
  );
`ifdef ASSUME_DEFINED_INPUTS
`endif
`ifndef DIRECT_CROSS_POINTS
`endif
`ifdef CHECK_MATCH_POINTS
`endif
`ifdef CHECK_OUTPUTS
  miter_cmp_prop #(1, "assert") \__po_text_out[60]$_DFF_P_.QN__assert (\__po_text_out[60]$_DFF_P_.QN__gold , \__po_text_out[60]$_DFF_P_.QN__gate );
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
  miter_def_prop #(1, "cover") \__po_text_out[60]$_DFF_P_.QN__gold_cover (\__po_text_out[60]$_DFF_P_.QN__gold );
`endif
`ifdef COVER_DEF_GATE_OUTPUTS
  miter_def_prop #(1, "cover") \__po_text_out[60]$_DFF_P_.QN__gate_cover (\__po_text_out[60]$_DFF_P_.QN__gate );
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
module \gold.aes_cipher_top.text_out.60_DFF_P_.QN (
  output [  0:0] \__po_text_out[60]$_DFF_P_.QN
);
endmodule
module \gate.aes_cipher_top.text_out.60_DFF_P_.QN (
  output [  0:0] \__po_text_out[60]$_DFF_P_.QN
);
endmodule
