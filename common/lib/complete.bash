#!/bin/bash
### lg bash complete
function lg_bash_complete {
	local prev cur opts
	COMPREPLY=()
	cur="${2}"
    prev="${1}"
	opts=$(cat $HOME/.lg/cmds.cache | xargs echo)
    COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
}
export -f lg_bash_complete
complete -F lg_bash_complete -A file lg
