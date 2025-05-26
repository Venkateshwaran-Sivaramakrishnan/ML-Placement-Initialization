yosys -ql run.log run.ys
if grep "SAT temporal induction proof finished - model found for base case: FAIL!" run.log > /dev/null ; then
	echo FAIL > status
	echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.121_DFF_P_.QN' using strategy 'basic'"
elif grep "Reached maximum number of time steps -> proof failed." run.log > /dev/null ; then
	echo UNKNOWN > status
	echo "Could not prove equivalence of partition 'aes_cipher_top.text_out.121_DFF_P_.QN' using strategy 'basic'"
elif grep "Induction step proven: SUCCESS!" run.log > /dev/null ; then
	echo PASS > status
	echo "Proved equivalence of partition 'aes_cipher_top.text_out.121_DFF_P_.QN' using strategy 'basic'"
else
	echo ERROR > status
	echo "Execution of strategy 'basic' on partition 'aes_cipher_top.text_out.121_DFF_P_.QN' encountered an error.
Details can be found in './logs/asap7/aes/base/4_eqy_output/strategies/aes_cipher_top.text_out.121_DFF_P_.QN/basic/run.log'."
	exit 1
fi
exit 0

