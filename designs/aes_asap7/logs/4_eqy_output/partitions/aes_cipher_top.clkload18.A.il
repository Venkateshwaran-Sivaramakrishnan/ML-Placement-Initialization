# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.clkload18.A
  attribute \keep 1
  wire input 1 \__pi_clkload17.A
  attribute \keep 1
  wire output 2 \__po_clkload18.A
  attribute \keep 1
  wire \clkload17.A
  attribute \keep 1
  wire \clkload18.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$22943
    connect \A \clkload17.A
    connect \Y \clkload18.A
  end
  connect \clkload17.A \__pi_clkload17.A
  connect \__po_clkload18.A \clkload18.A
end
module \gold.aes_cipher_top.clkload18.A
  attribute \keep 1
  wire input 1 \__pi_clkload17.A
  attribute \keep 1
  wire output 2 \__po_clkload18.A
  attribute \keep 1
  wire \clkload17.A
  attribute \keep 1
  wire \clkload18.A
  cell $_BUF_ $auto$insbuf.cc:97:execute$19718
    connect \A \clkload17.A
    connect \Y \clkload18.A
  end
  connect \clkload17.A \__pi_clkload17.A
  connect \__po_clkload18.A \clkload18.A
end
