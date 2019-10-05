#!/usr/bin/env bash

current_path=$(pwd)

# install alibaba arthas
echo -e "$(tput bold)install alibaba arthas...$(tput sgr0)"
curl -L https://alibaba.github.io/arthas/install.sh | sh
sed -i '' 's/.\/as.sh/${0}/g' as.sh
mv as.sh ${current_path}/custom/tools/arthas
