#!/bin/bash
### ldf bash complete
function ldf_bash_complete {
	local prev cur opts
	COMPREPLY=()
	cur="${2}"
    prev="${1}"
	opts=$(cat $HOME/.ldf/cmds.cache | xargs echo)
    COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
}
export -f ldf_bash_complete
complete -F ldf_bash_complete -A file ldf
