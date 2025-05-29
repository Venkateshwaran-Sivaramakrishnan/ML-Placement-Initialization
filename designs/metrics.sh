#!/bin/bash

if [[ $# -lt 1 ]]; then
  echo "usage: ./metrics.sh <design> <process>"
  echo "usage: ./metrics.sh <csv_file>"
  exit 1
fi

get_metrics() {
  # LOGS_DIR="${DESIGN}_${PROCESS}/logs"
  LOGS_DIR=$1

  HPWL_FILE="${LOGS_DIR}/3_5_place_dp.json"
  RUNTIME_FILE="${LOGS_DIR}/3_3_place_gp.log"

  HPWL=$(awk '/detailedplace__route__wirelength__estimated/ { print $2 }' ${HPWL_FILE} | cut -d , -f1)
  ITERATIONS=$(tac ${RUNTIME_FILE} | awk '/\[NesterovSolve\] Iter:/ { print $3; exit}')
  RUNTIME=$(tail -n 1 ${RUNTIME_FILE} | awk '/Elapsed time:/ { print $3; exit }' | awk -F\[ '{ print $1 }')

  echo "${HPWL}|${ITERATIONS}|${RUNTIME}"
}

if [[ $# -ne 1 ]]; then
  LOGS_DIR="${1}_${2}/logs"
  RESULTS=$(get_metrics ${LOGS_DIR})
  IFS=" " read -r HPWL ITERATIONS RUNTIME <<< "${RESULTS}"
  echo "Stats from ${1}_${2}"
  echo "---------------------"
  echo "Estimated HPWL: ${HPWL}"
  echo "Number of NesterovSolve Iterations: ${ITERATIONS}"
  echo "Total runtime (h:m:ss): ${RUNTIME}"
else
  echo "DESIGN,PROCESS,HPWL,ITERATIONS,RUNTIME" > $1
  for directory in **/logs; do
    DESIGN_INFO=$(dirname ${directory} | sed 's/_/,/g')
    RESULTS=$(get_metrics ${directory})
    if [ "${RESULTS}" != "||" ]; then
      IFS="|" read -r HPWL ITERATIONS RUNTIME <<< "${RESULTS}"
      echo "${DESIGN_INFO},${HPWL},${ITERATIONS},${RUNTIME}" >> $1
    fi
  done
fi
