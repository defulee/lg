#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "ldf" ] &&
	git clone --depth 1 https://github.com/defulee/ldf.git 
    cd ldf
    make install
    source ldf-complete
fi
