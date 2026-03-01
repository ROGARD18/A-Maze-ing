VENV_NAME := a_maze_ing_env
NAME := a_maze_ing.py
CONFIG_FILE := config.txt
OUTPUT_FILE := maze.txt

install:
	python3 -m venv $(VENV_NAME)
	source a_maze_ing_venv/bin/source
	pip -r requierements.txt

run:
	python3 $(NAME) $(CONFIG_FILE)

debug:

clean:
	rm $(OUTPUT_FILE)
	mypy_cache
	__pycache__

lint:
	flake8 . && mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	flake8 . && mypy . --strict