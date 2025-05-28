STATUS=ERROR
sby -f jpeg_encoder.clknet_leaf_106_clk.sby > /dev/null && STATUS=$(awk '{print $1}' jpeg_encoder.clknet_leaf_106_clk/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'jpeg_encoder.clknet_leaf_106_clk' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'jpeg_encoder.clknet_leaf_106_clk' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'jpeg_encoder.clknet_leaf_106_clk' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'jpeg_encoder.clknet_leaf_106_clk' using strategy 'sby': timeout"
    ;;
    *)
        cat jpeg_encoder.clknet_leaf_106_clk/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'jpeg_encoder.clknet_leaf_106_clk' encountered an error."
        echo "More details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.clknet_leaf_106_clk/sby/jpeg_encoder.clknet_leaf_106_clk/logfile.txt'."
        exit 1
    ;;
esac
exit 0

