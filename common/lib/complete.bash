#!/bin/bash
### bash complete
function bash_complete {
	local prev cur opts
	COMPREPLY=()
	cur="${2}"
    prev="${1}"
	opts=$(cat $HOME/.ftool/cmds.cache | xargs echo)
    COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
}
export -f bash_complete
complete -F bash_complete -A file ftool
