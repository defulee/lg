#!/bin/zsh
### tb zsh complete
function zsh_complete {
	reply=(
	$(cat $HOME/.tb/cmds.cache|xargs echo)
	)
}
compctl -K zsh_complete tb
