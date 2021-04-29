#!/usr/bin/env make

.PHONY: %

database:
	docker-compose up -d

import:
	python -c 'from db_update import update_db; update_db()'
