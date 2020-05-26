#!/bin/bash

export LDF_DIR=$(dirname "$(echo "$0" | sed -e '')")

# load rcfile
rcfile="${LDF_DIR}/ldfrc"
[ -r "${rcfile}" ] && source "${rcfile}"
export ldf_custom_rcfile="${HOME}/.ldfrc"
[ -r "${ldf_custom_rcfile}" ] && source "${ldf_custom_rcfile}"

# load common lib functions
common_lib="${LDF_DIR}/common/lib/common-functions"
[ -r "${common_lib}" ] && source ${common_lib}

logo() {
    echo '
       _          
      //  __/   /)
    _(/__(_/(__//_
            _/   
            /)   
            `           
    '
}
usage() {
cat << EOF
$(fmt_bold USAGE)
ldf list:       show all commands 
ldf command:    execute a command(such as color、stats)
ldf update:     update ldf
ldf uninstall:  uninstall ldf
EOF
}

find_commands() {
    for folder in `ls -l $1 | grep ^d | awk '{print $9}'` ;do
        tools_dir="$1/${folder}/tools"
        if [ ! -d ${tools_dir} ]; then
            continue;
        fi
        cmds=`ls -l ${tools_dir} | grep -v '^d' | awk '{print $9}'`
        if [ "${cmds}" = "" ]; then
            continue;
        fi

        fmt_title ${folder} 
        for cmd in ${cmds} ;do
            desc=`grep '^###' ${tools_dir}/${cmd} | cut -c 4-`
            if [ "${desc}" != ""  ]; then
                fmt_cmd "${cmd}\t:$desc"
                echo "${cmd}" >> $HOME/.ldf/cmds.cache
            fi
        done
        echo ''
    done

}

list() {
    rm -f $HOME/.ldf/cmds.cache 2>/dev/null
    mkdir $HOME/.ldf 2>/dev/null
    echo 'Available commands:'
    find_commands ${LDF_DIR}
    find_commands ${LDF_DIR}/custom
    exit 0;
}

uninstall() {
    echo -n "Uninstall ldf,(y)es or (n)o?"
    read choice < /dev/tty
    if [ "${choice}" = "y" ] && [ "${LDF_DIR}" != "/" ];then
	    cd ${LDF_DIR} && make uninstall && rm -rf ${LDF_DIR} && echo "ldf uninstall finished. Bye~"
    fi
    exit 0
}

if [ $# = 0 ];then
    logo
    usage
    exit
fi

if [ "$1" = "list" ];then 
    list "$@"
fi

if [ "$1" = "uninstall" ]; then
    uninstall "$@"
fi

tools_dir=${LDF_DIR}/*/tools/
custom_tools_dir=${LDF_DIR}/custom/*/tools/
command_file=$1;shift
command=`find ${tools_dir} -maxdepth 1 -name ${command_file} `

if [ ! -f "${command}" ]; then
    command=`find ${custom_tools_dir} -maxdepth 1 -name ${command_file} `
    if [ ! -f "${command}" ]; then
	echo "${command_file} command not found!"
	exit 1;
    fi
fi

exec "${command}" "$@"

