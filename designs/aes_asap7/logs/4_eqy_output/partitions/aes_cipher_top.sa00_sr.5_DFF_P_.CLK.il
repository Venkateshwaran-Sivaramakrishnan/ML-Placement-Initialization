# Generated by Yosys 0.51+85 (git sha1 d3aec12fe, clang++ 18.1.8 -fPIC -O3)
autoidx 25246
module \gate.aes_cipher_top.sa00_sr.5_DFF_P_.CLK
  attribute \keep 1
  wire input 1 \__pi_sa00_sr[4]$_DFF_P_.CLK
  attribute \keep 1
  wire output 2 \__po_sa00_sr[5]$_DFF_P_.CLK
  attribute \keep 1
  wire \sa00_sr[4]$_DFF_P_.CLK
  attribute \keep 1
  wire \sa00_sr[5]$_DFF_P_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$24182
    connect \A \sa00_sr[4]$_DFF_P_.CLK
    connect \Y \sa00_sr[5]$_DFF_P_.CLK
  end
  connect \sa00_sr[4]$_DFF_P_.CLK \__pi_sa00_sr[4]$_DFF_P_.CLK
  connect \__po_sa00_sr[5]$_DFF_P_.CLK \sa00_sr[5]$_DFF_P_.CLK
end
module \gold.aes_cipher_top.sa00_sr.5_DFF_P_.CLK
  attribute \keep 1
  wire input 1 \__pi_sa00_sr[4]$_DFF_P_.CLK
  attribute \keep 1
  wire output 2 \__po_sa00_sr[5]$_DFF_P_.CLK
  attribute \keep 1
  wire \sa00_sr[4]$_DFF_P_.CLK
  attribute \keep 1
  wire \sa00_sr[5]$_DFF_P_.CLK
  cell $_BUF_ $auto$insbuf.cc:97:execute$20957
    connect \A \sa00_sr[4]$_DFF_P_.CLK
    connect \Y \sa00_sr[5]$_DFF_P_.CLK
  end
  connect \sa00_sr[4]$_DFF_P_.CLK \__pi_sa00_sr[4]$_DFF_P_.CLK
  connect \__po_sa00_sr[5]$_DFF_P_.CLK \sa00_sr[5]$_DFF_P_.CLK
end
