#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: ./metrics.sh <design> <process>"
  exit 1
fi

DESIGN=$1
PROCESS=$2

LOGS_DIR="${DESIGN}_${PROCESS}/logs"

HPWL_FILE="${LOGS_DIR}/3_5_place_dp.json"
RUNTIME_FILE="${LOGS_DIR}/3_3_place_gp.log"

HPWL=$(awk '/detailedplace__route__wirelength__estimated/ { print $2 }' ${HPWL_FILE} | cut -d , -f1)
ITERATIONS=$(tac ${RUNTIME_FILE} | awk '/\[NesterovSolve\] Iter:/ { print $3; exit}')
RUNTIME=$(tail -n 1 ${RUNTIME_FILE} | awk '/Elapsed time:/ { print $3; exit }' | awk -F[ '{ print $1 }')

echo "Reading from ${HPWL_FILE} and ${RUNTIME_FILE}"
echo "---------------------"
echo "Estimated HPWL: ${HPWL}"
echo "Number of NesterovSolve Iterations: ${ITERATIONS}"
echo "Total runtime (h:m:ss): ${RUNTIME}"
