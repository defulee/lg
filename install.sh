#!/bin/bash

if command -v git &> /dev/null; then
	[ ! -d "ftool" ] &&
	git clone --depth 1 https://github.com/defulee/toolbox.git
  cd ftool

  echo -e "$(tput bold)prepare install custom tools...$(tput sgr0)"
  ./custom/install.sh

  echo -e "$(tput bold)prepare install tools...$(tput sgr0)"
  make install
  source complete
fi
