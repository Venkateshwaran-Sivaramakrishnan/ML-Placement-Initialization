# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 81787
module \gate.jpeg_encoder.output28.Y
  attribute \keep 1
  wire input 1 \__pi_output28.A
  attribute \keep 1
  wire output 2 \__po_output28.Y
  attribute \keep 1
  wire \output28.A
  attribute \keep 1
  wire \output28.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$80783
    connect \A \output28.A
    connect \Y \output28.Y
  end
  connect \output28.A \__pi_output28.A
  connect \__po_output28.Y \output28.Y
end
module \gold.jpeg_encoder.output28.Y
  attribute \keep 1
  wire input 1 \__pi_output28.A
  attribute \keep 1
  wire output 2 \__po_output28.Y
  attribute \keep 1
  wire \output28.A
  attribute \keep 1
  wire \output28.Y
  cell $_BUF_ $auto$insbuf.cc:97:execute$68868
    connect \A \output28.A
    connect \Y \output28.Y
  end
  connect \output28.A \__pi_output28.A
  connect \__po_output28.Y \output28.Y
end
