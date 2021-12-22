#!/bin/zsh
### tb zsh complete
function st_zsh_complete {
	reply=(
	$(cat $HOME/.st/cmds.cache|xargs echo)
	)
}
compctl -K st_zsh_complete st
