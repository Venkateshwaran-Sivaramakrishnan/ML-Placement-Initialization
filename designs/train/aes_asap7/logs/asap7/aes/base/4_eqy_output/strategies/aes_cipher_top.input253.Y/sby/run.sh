STATUS=ERROR
sby -f aes_cipher_top.input253.Y.sby > /dev/null && STATUS=$(awk '{print $1}' aes_cipher_top.input253.Y/status)
echo $STATUS > status
case $STATUS in
    PASS)
        echo "Proved equivalence of partition 'aes_cipher_top.input253.Y' using strategy 'sby'"
    ;;
    FAIL)
        echo "Could not prove equivalence of partition 'aes_cipher_top.input253.Y' using strategy 'sby': partitions not equivalent"
    ;;
    UNKNOWN)
        echo "Could not prove equivalence of partition 'aes_cipher_top.input253.Y' using strategy 'sby': equivalence unknown"
    ;;
    TIMEOUT)
        echo "Could not prove equivalence of partition 'aes_cipher_top.input253.Y' using strategy 'sby': timeout"
    ;;
    *)
        cat aes_cipher_top.input253.Y/ERROR 2> /dev/null
        echo "Execution of strategy 'sby' on partition 'aes_cipher_top.input253.Y' encountered an error."
        echo "More details can be found in './logs/asap7/aes/base/4_eqy_output/strategies/aes_cipher_top.input253.Y/sby/aes_cipher_top.input253.Y/logfile.txt'."
        exit 1
    ;;
esac
exit 0

