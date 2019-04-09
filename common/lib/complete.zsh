#!/bin/zsh
### ldf zsh complete
function ldf_zsh_complete {
	reply=(
	$(cat $HOME/.ldf/cmds.cache|xargs echo)
	)
}
compctl -K ldf_zsh_complete ldf
