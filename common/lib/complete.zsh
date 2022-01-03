#!/bin/zsh
### zsh complete
function zsh_complete {
	reply=(
	$(cat $HOME/.ftool/cmds.cache|xargs echo)
	)
}
compctl -K zsh_complete ftool
