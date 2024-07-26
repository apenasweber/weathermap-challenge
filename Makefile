# Variables
PYTHON = python3
ISORT = isort
BLACK = black
FLAKE8 = flake8
PYLINT = pylint
PYTEST = pytest

# Paths
SRC_DIR = app
TEST_DIR = tests

# Commands
.PHONY: all format lint test fix

all: format lint test

format: isort black

isort:
	$(ISORT) $(SRC_DIR) $(TEST_DIR)

black:
	$(BLACK) $(SRC_DIR) $(TEST_DIR)

lint: isort_lint black_lint flake8 pylint

isort_lint:
	$(ISORT) --check-only $(SRC_DIR) $(TEST_DIR)

black_lint:
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR)

flake8:
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR)

pylint:
	$(PYLINT) $(SRC_DIR) $(TEST_DIR)

tests:
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=term-missing -W ignore::DeprecationWarning

fix: isort black
	$(ISORT) $(SRC_DIR) $(TEST_DIR)
	$(BLACK) $(SRC_DIR) $(TEST_DIR)
