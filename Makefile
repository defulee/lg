
target_loc=/usr/local/bin/
target_app='/usr/local/bin/lg'

all:
	@echo "usage: make install"
	@echo "       make uninstall"

install:
	@mkdir -p $(target_loc)
	@echo '#!/bin/bash' > $(target_app)
	@echo '##$(shell pwd)' >> $(target_app)
	@echo 'exec "$(shell pwd)/lgo" "$$@"' >> $(target_app)
	@chmod 755 ${target_app}
	@echo 'install finished! type "lg" to show usages.'
uninstall:
	@rm -f ${target_app}

