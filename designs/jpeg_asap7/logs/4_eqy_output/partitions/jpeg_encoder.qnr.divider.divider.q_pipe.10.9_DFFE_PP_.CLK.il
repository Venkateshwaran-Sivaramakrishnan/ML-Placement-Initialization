# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.qnr.divider.divider.q_pipe.10.9_DFFE_PP_.CLK
  attribute \keep 1
  wire input 1 \__pi_qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  attribute \keep 1
  wire output 2 \__po_qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  attribute \keep 1
  wire \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  attribute \keep 1
  wire \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$81021
    connect \A \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
    connect \Y \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  end
  connect \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK \__pi_qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  connect \__po_qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
end
module \gold.jpeg_encoder.qnr.divider.divider.q_pipe.10.9_DFFE_PP_.CLK
  attribute \keep 1
  wire input 1 \__pi_qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  attribute \keep 1
  wire output 2 \__po_qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  attribute \keep 1
  wire \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  attribute \keep 1
  wire \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$69106
    connect \A \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
    connect \Y \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
  end
  connect \qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK \__pi_qnr.divider.divider.q_pipe[10][8]$_DFFE_PP_.CLK
  connect \__po_qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK \qnr.divider.divider.q_pipe[10][9]$_DFFE_PP_.CLK
end
