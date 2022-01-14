PYTHON = python

.PHONY = help setup test build

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To build the project type \"make build\""
	@echo "To setup the project type \"make setup\""
	@echo "To test the project type \"make test\""
	@echo "------------------------------------"

setup:
	@echo "Installing dependencies ..."
	pip install -r requirements.txt

test:
	@echo "Running Unit tests ..."
	${PYTHON} -m unittest "tests/test_api.py"

build: | setup test
