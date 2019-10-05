#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "ldf" ] &&
	git clone --depth 1 https://github.com/defulee/ldf.git 
    cd ldf

    echo -e "\e[1;34m prepare install custom tools... \e[0m"
    ./custom/install.sh

    echo -e "\e[1;34m prepare make install ldf to path... \e[0m"
    make install
    source ldf-complete
fi
