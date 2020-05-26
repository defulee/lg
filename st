#!/bin/bash

export st_DIR=$(dirname "$(echo "$0" | sed -e '')")

# load rcfile
rcfile="${st_DIR}/strc"
[ -r "${rcfile}" ] && source "${rcfile}"
export st_custom_rcfile="${HOME}/.strc"
[ -r "${st_custom_rcfile}" ] && source "${st_custom_rcfile}"

# load common lib functions
common_lib="${st_DIR}/common/lib/common-functions"
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
st list:       show all commands 
st command:    execute a command(such as color、stats)
st update:     update st
st uninstall:  uninstall st
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
                echo "${cmd}" >> $HOME/.st/cmds.cache
            fi
        done
        echo ''
    done

}

list() {
    rm -f $HOME/.st/cmds.cache 2>/dev/null
    mkdir $HOME/.st 2>/dev/null
    echo 'Available commands:'
    find_commands ${st_DIR}
    find_commands ${st_DIR}/custom
    exit 0;
}

uninstall() {
    echo -n "Uninstall st,(y)es or (n)o?"
    read choice < /dev/tty
    if [ "${choice}" = "y" ] && [ "${st_DIR}" != "/" ];then
	    cd ${st_DIR} && make uninstall && rm -rf ${st_DIR} && echo "st uninstall finished. Bye~"
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

tools_dir=${st_DIR}/*/tools/
custom_tools_dir=${st_DIR}/custom/*/tools/
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

