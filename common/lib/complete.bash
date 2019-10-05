#!/bin/bash
### moto bash complete
function moto_bash_complete {
	local prev cur opts
	COMPREPLY=()
	cur="${2}"
    prev="${1}"
	opts=$(cat $HOME/.moto/cmds.cache | xargs echo)
    COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
}
export -f moto_bash_complete
complete -F moto_bash_complete -A file moto
