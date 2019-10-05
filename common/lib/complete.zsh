#!/bin/zsh
### moto zsh complete
function moto_zsh_complete {
	reply=(
	$(cat $HOME/.moto/cmds.cache|xargs echo)
	)
}
compctl -K moto_zsh_complete moto
