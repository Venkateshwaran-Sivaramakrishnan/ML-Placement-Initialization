STATUS=ERROR
sby -f jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN.sby > /dev/null && STATUS=$(awk '{print $1}' jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN' using strategy 'sby': timeout"
    ;;
    *)
        cat jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN' encountered an error."
        echo "More details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN/sby/jpeg_encoder.rle.rz4.rleno.3_DFFE_PP_.QN/logfile.txt'."
        exit 1
    ;;
esac
exit 0

