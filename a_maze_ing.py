from pydantic import ValidationError
from dotenv import load_dotenv
from os import getenv
from random import seed, random

from utils.check_dep import check_dep
from utils.parsing import parsing
from MazeGen.generator import Maze_Generator


def main() -> None:
    config: Config | None = None
    try:
        print("Checking if all dependencies are installed...")
        check_dep()
        print("Deps well installed.\n")
    except Exception as e:
        print(e)
        print("line 20")
        return
    try:
        print("Parsing config file...")
        config = parsing()
        if not config:
            raise ValueError("Error: try with config.txt to refere some"
                             " parameters for the maze.")
        print("Config acquired")
    except (ValidationError, KeyError) as e:
        print(f"{type(e).__name__}: {e}")
        return
    load_dotenv()
    maze_seed: str | None = getenv("seed")
    if maze_seed:
        seed(float(maze_seed))
    else:
        maze_seed = str(random())
        seed(float(maze_seed))
    print(f"seed: {maze_seed}")

    from menu.menu import menu_loop
    menu_loop(config)


if __name__ == "__main__":
    main()
