#!/usr/bin/env make

.PHONY: %

database:
	docker-compose up -d

import:
	python -c 'from db_update import update_db; update_db()'

tests:
	pip install -r requirements.txt
	docker-compose up -d
	pytest
	docker-compose down
