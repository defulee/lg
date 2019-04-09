#!/bin/zsh
### lg zsh complete
function lg_zsh_complete {
	reply=(
	$(cat $HOME/.lg/cmds.cache|xargs echo)
	)
}
compctl -K lg_zsh_complete lg
