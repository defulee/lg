#!/usr/bin/env bash

current_path=$(pwd)
test -d "${current_path}/custom/tools" || mkdir -p ${current_path}/custom/tools

# install alibaba arthas
echo -e "$(tput bold)install alibaba arthas...$(tput sgr0)"
curl -L https://alibaba.github.io/arthas/install.sh | sh
sed -i '' 's/.\/as.sh/arthas/g' as.sh
mv as.sh ${current_path}/custom/tools/arthas
