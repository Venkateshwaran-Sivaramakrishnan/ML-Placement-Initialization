STATUS=ERROR
sby -f aes_cipher_top.text_out.75.sby > /dev/null && STATUS=$(awk '{print $1}' aes_cipher_top.text_out.75/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'aes_cipher_top.text_out.75' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.75' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.75' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.75' using strategy 'sby': timeout"
    ;;
    *)
        cat aes_cipher_top.text_out.75/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'aes_cipher_top.text_out.75' encountered an error."
        echo "More details can be found in './logs/asap7/aes/base/4_eqy_output/strategies/aes_cipher_top.text_out.75/sby/aes_cipher_top.text_out.75/logfile.txt'."
        exit 1
    ;;
esac
exit 0

