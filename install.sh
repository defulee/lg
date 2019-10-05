#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "ldf" ] &&
	git clone --depth 1 https://github.com/defulee/ldf.git 
    cd ldf

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    ./custom/install.sh

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    make install
    source ldf-complete
fi
