VENV_NAME := a_maze_ing_env
NAME := a_maze_ing.py
CONFIG_FILE := config.txt
OUTPUT_FILE := maze.txt
FLAKE8 := poetry run flake8
MYPY := poetry run mypy
PYTHON := poetry run python3

install:
	@poetry install
	

run:
	@$(PYTHON) $(NAME) $(CONFIG_FILE)

debug:

clean:
	@rm $(OUTPUT_FILE)
	@rm -f **/**mypy_cache
	@rm -rf **/**__pycache__

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict