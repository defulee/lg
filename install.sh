#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "ldf" ] &&
	git clone --depth 1 https://github.com/defulee/ldf.git 
    cd ldf
    export LDF_DIR=$(dirname "$(echo "$0" | sed -e '')")
    ./custom/install.sh
    make install
    source ldf-complete
fi
