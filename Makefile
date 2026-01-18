#
# Makefile for A-Maze-ing by afomin and andmarti
#

GREEN = \033[1;92m
YELLOW = \033[1;93m
RESET = \033[0m
FLAKEFLAGS = --exclude venv
MYPYFLAGS= --exclude venv \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

venv:
	@echo "$(YELLOW)venv loading...$(RESET)"
	@test -d venv || python3 -m venv venv
	@echo "$(GREEN)venv created.$(RESET)"

install:
	pip install --upgrade pip && \
	pip install flake8 mypy

run:
	python3 main.py $(CONFIG)

debug:
	python3 -m pdb main.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[co]" -delete

lint:
	@echo "$(GREEN)==============$(RESET)"
	@echo "$(GREEN)=== flake8 ===$(RESET)"
	@echo "$(GREEN)==============$(RESET)"
	@flake8 . $(FLAKEFLAGS) || true
	@echo "$(GREEN)============$(RESET)"
	@echo "$(GREEN)=== mypy ===$(RESET)"
	@echo "$(GREEN)============$(RESET)"
	@mypy . $(MYPYFLAGS) || true

