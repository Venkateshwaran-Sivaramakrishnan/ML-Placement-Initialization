#!/bin/bash

if [[ $# -lt 2 ]]; then
  echo "usage: ./migrate.sh <design> <process> [dry-run]"
  exit 1
fi

DESIGN=$1
PROCESS=$2
DRY_RUN=$3


migrate_folder() {
  FOLDER=$1

  ORIGINAL_LOCATION="${DESIGN}_${PROCESS}/${FOLDER}/${PROCESS}/${DESIGN}/base"

  if [ ! -e "${ORIGINAL_LOCATION}" ]; then
    echo "${ORIGINAL_LOCATION} doesn't exist!"
    exit 1;
  fi

  if [[ -n "${DRY_RUN}" ]]; then
    echo -e "${ORIGINAL_LOCATION}/* -> ${DESIGN}_${PROCESS}/${FOLDER}"
  else
    mv ${ORIGINAL_LOCATION}/* "${DESIGN}_${PROCESS}/${FOLDER}"
    rm -rf "${ORIGINAL_LOCATION}"
  fi
}

migrate_folder logs
migrate_folder objects
migrate_folder reports
migrate_folder results
