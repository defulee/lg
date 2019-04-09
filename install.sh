#!/bin/bash

export LG_DIR=$(dirname "$(echo "$0" | sed -e '')")

make -f ${LG_DIR}/Makefile install

source ${LG_DIR}/lg-complete