#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "qu" ] &&
	git clone --depth 1 https://github.com/defulee/st.git 
    cd qu

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    ./custom/install.sh

    echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
    make install
    source st-complete
fi
