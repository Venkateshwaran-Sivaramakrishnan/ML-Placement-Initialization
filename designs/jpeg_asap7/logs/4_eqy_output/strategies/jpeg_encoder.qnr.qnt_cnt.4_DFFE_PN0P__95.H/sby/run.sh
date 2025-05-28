STATUS=ERROR
sby -f jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H.sby > /dev/null && STATUS=$(awk '{print $1}' jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H' using strategy 'sby': timeout"
    ;;
    *)
        cat jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H' encountered an error."
        echo "More details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H/sby/jpeg_encoder.qnr.qnt_cnt.4_DFFE_PN0P__95.H/logfile.txt'."
        exit 1
    ;;
esac
exit 0

