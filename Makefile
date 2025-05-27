# Makefile

VENV := .venv
PYTHON := $(VENV)/bin/python
UV := uv
PYTEST := $(VENV)/bin/pytest

.PHONY: help venv install test clean

help:
	@echo "Makefile commands:"
	@echo "  venv       - Create virtual environment"
	@echo "  install    - Install dependencies from pyproject.toml"
	@echo "  test       - Run pytest tests"
	@echo "  clean      - Remove virtual environment and __pycache__"

venv:
	@echo "Creating virtual environment in $(VENV)..."
	$(UV) venv $(VENV)

install: venv
	@echo "Installing dependencies with uv..."
	$(UV) pip install --upgrade pip
	$(UV) pip install -e .
	# or just: $(UV) pip install .

test:
	@echo "Running tests with pytest..."
	$(PYTEST)

clean:
	@echo "Removing virtual environment and __pycache__..."
	rm -rf $(VENV) **/__pycache__
