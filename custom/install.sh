#!/usr/bin/env bash

# load rcfile
rcfile="${LDF_DIR}/ldfrc"
[ -r "${rcfile}" ] && source "${rcfile}"
export ldf_custom_rcfile="${HOME}/.ldfrc"
[ -r "${ldf_custom_rcfile}" ] && source "${ldf_custom_rcfile}"

# load common lib functions
common_lib="${LDF_DIR}/common/lib/common-functions"
[ -r "${common_lib}" ] && source ${common_lib}

current_path=$(pwd)

# install alibaba arthas
bprint "install alibaba arthas..."
curl -L https://alibaba.github.io/arthas/install.sh | sh
sed -i '' 's/.\/as.sh/${0}/g' as.sh
mv as.sh ${current_path}/ldf/custom/tools/arthas
