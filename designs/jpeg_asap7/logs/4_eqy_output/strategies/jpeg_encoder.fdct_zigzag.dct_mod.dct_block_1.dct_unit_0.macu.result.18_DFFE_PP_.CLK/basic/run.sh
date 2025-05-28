yosys -ql run.log run.ys
if grep "SAT temporal induction proof finished - model found for base case: FAIL!" run.log > /dev/null ; then
	echo FAIL > status
	echo "Could not prove equivalence of partition 'jpeg_encoder.fdct_zigzag.dct_mod.dct_block_1.dct_unit_0.macu.result.18_DFFE_PP_.CLK' using strategy 'basic'"
elif grep "Reached maximum number of time steps -> proof failed." run.log > /dev/null ; then
	echo UNKNOWN > status
	echo "Could not prove equivalence of partition 'jpeg_encoder.fdct_zigzag.dct_mod.dct_block_1.dct_unit_0.macu.result.18_DFFE_PP_.CLK' using strategy 'basic'"
elif grep "Induction step proven: SUCCESS!" run.log > /dev/null ; then
	echo PASS > status
	echo "Proved equivalence of partition 'jpeg_encoder.fdct_zigzag.dct_mod.dct_block_1.dct_unit_0.macu.result.18_DFFE_PP_.CLK' using strategy 'basic'"
else
	echo ERROR > status
	echo "Execution of strategy 'basic' on partition 'jpeg_encoder.fdct_zigzag.dct_mod.dct_block_1.dct_unit_0.macu.result.18_DFFE_PP_.CLK' encountered an error.
Details can be found in './logs/asap7/jpeg/base/4_eqy_output/strategies/jpeg_encoder.fdct_zigzag.dct_mod.dct_block_1.dct_unit_0.macu.result.18_DFFE_PP_.CLK/basic/run.log'."
	exit 1
fi
exit 0

