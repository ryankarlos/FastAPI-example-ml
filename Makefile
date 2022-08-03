VENV = venv
PYTHON = python3.8

.PHONY: all run test clean install help

all: dev


#install: src/requirements-dev.txt src/requirements.txt
#	${PYTHON} -m venv ${VENV}
#	${VENV}/bin/pip install -r src/requirements-dev.txt
#   ${VENV}/bin/pip install -r src/requirements.txt
#	. ${VENV}/bin/activate && exec bash

help:
	@echo "---------------HELP-----------------"
	@echo "To setup a container for development, type 'make'"
	@echo "To run the tests type 'make test'"
	@echo "To run all the crud operations and train model/predictions type 'make run'"
	@echo "To clean the venv folder,cache and docker images type 'make clean'"
	@echo "------------------------------------"


load: docker-compose.yml
	docker compose run dev -c "python -m src.load_data_into_tables"

run: docker-compose.yml
	docker compose run dev -c "python -m src.app.crud"

dev: docker-compose.yml
	docker compose run dev

web: docker-compose.yml
	docker compose run -d webapp

stop: docker-compose.yml
	docker compose down

test: docker-compose.yml
	docker compose run unittest

# needs double $,otherwise makefile interprets it as makefile variables and returns only docker rmi
clean:
	rm -rf __pycache__
	rm -rf ${VENV}
	make stop
	docker rmi $$(docker images)
