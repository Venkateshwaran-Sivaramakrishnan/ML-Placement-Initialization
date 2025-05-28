#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: ./import.sh <design> <process> [dry-run]"
  exit 1
fi

DESIGN=$1
PROCESS=$2
DRY_RUN=$3

ORFS_DIR="../OpenROAD-flow-scripts/flow"

import_from_orfs() {
  FOLDER=$1

  SOURCE_DIR="${ORFS_DIR}/${FOLDER}/${PROCESS}/${DESIGN}/base"
  TARGET_DIR="${DESIGN}_${PROCESS}/${FOLDER}"

  if [ ! -e "${SOURCE_DIR}" ]; then
    echo "${SOURCE_DIR} doesn't exist!"
    exit 1;
  fi

  if [[ -n "${DRY_RUN}" ]]; then
    echo -e "${SOURCE_DIR}/* -> ${TARGET_DIR}"
  else
    mkdir -p ${TARGET_DIR}
    cp -r ${SOURCE_DIR}/* ${TARGET_DIR}
  fi
}

import_from_orfs logs
import_from_orfs objects
import_from_orfs reports
import_from_orfs results
