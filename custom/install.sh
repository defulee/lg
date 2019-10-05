#!/usr/bin/env bash

# install alibaba arthas
curl -L https://alibaba.github.io/arthas/install.sh | sh
sed -i '' 's/.\/as.sh/${0}/g' as.sh
mv as.sh tools/arthas
