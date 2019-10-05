#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "moto" ] &&
	git clone --depth 1 https://github.com/defulee/moto.git 
    cd moto

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    ./custom/install.sh

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    make install
    source moto-complete
fi
