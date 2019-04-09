#!/bin/bash
### lg bash complete
function lg_sh_complete {
	local prev cur opts
	COMPREPLY=()
	cur="${2}"
    prev="${1}"
	opts=$(cat $HOME/.lg/cmds.cache | xargs echo)
    COMPREPLY=( $( compgen -W "$opts" -- $cur ) )
}
export -f lg_sh_complete
complete -F lg_sh_completes -A file lg
