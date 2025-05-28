STATUS=ERROR
sby -f aes_cipher_top.text_out.61.sby > /dev/null && STATUS=$(awk '{print $1}' aes_cipher_top.text_out.61/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'aes_cipher_top.text_out.61' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.61' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.61' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.61' using strategy 'sby': timeout"
    ;;
    *)
        cat aes_cipher_top.text_out.61/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'aes_cipher_top.text_out.61' encountered an error."
        echo "More details can be found in './logs/asap7/aes/base/4_eqy_output/strategies/aes_cipher_top.text_out.61/sby/aes_cipher_top.text_out.61/logfile.txt'."
        exit 1
    ;;
esac
exit 0

