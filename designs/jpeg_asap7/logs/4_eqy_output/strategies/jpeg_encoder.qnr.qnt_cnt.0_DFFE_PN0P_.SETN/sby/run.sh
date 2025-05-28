STATUS=ERROR
sby -f jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN.sby > /dev/null && STATUS=$(awk '{print $1}' jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN' using strategy 'sby': timeout"
    ;;
    *)
        cat jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN' encountered an error."
        echo "More details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN/sby/jpeg_encoder.qnr.qnt_cnt.0_DFFE_PN0P_.SETN/logfile.txt'."
        exit 1
    ;;
esac
exit 0

