#!/bin/bash

export LDF_DIR=$(dirname "$(echo "$0" | sed -e '')")

make -f ${LDF_DIR}/Makefile install

source ${LDF_DIR}/ldf-complete