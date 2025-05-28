STATUS=ERROR
sby -f jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK.sby > /dev/null && STATUS=$(awk '{print $1}' jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK' using strategy 'sby': timeout"
    ;;
    *)
        cat jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK' encountered an error."
        echo "More details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK/sby/jpeg_encoder.fdct_zigzag.zigzag_mod.sresult.33.5_DFFE_PP_.CLK/logfile.txt'."
        exit 1
    ;;
esac
exit 0

