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
	@rm -f $(OUTPUT_FILE)
	@rm -f **/**mypy_cache
	@rm -rf **/**__pycache__
	@rm -rf .mypy_cache
	@echo "  ______   __"
	@echo " /      \ /  |                                                _"
	@echo "/000000  |00 |  ______    ______   _______                   //"
	@echo "00 |  00/ 00 | /      \  /      \ /       \                 //"
	@echo "00 |      00 |/000000  | 000000  |0000000  |               //"
	@echo "00 |   __ 00 |00    00 | /    00 |00 |  00 |              //"
	@echo "00 \__/  |00 |00000000/ /0000000 |00 |  00 |             //"
	@echo "00    00/ 00 |00       |00    00 |00 |  00 |            //"
	@echo " 000000/  00/  0000000/  0000000/ 00/   00/            //"
	@echo "                                              ________//_______"
	@echo "                                             |################|"
	@echo "                                              ################ "
	@echo ""
	@echo "                                         . : .  *    ."
	@echo "                                        . : *. * . : * . ."
	@echo "                                       :: *   ..  : . *"
	@echo "                                      * . *:   *   . * .  ."

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict

