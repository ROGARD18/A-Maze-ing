from pydantic import ValidationError
from dotenv import load_dotenv
from os import getenv
from random import seed, random
from utils.models import Config
from utils.check_dep import check_dep
from utils.parsing import parsing
from utils.models import Config
from MazeGen.generator import MazeGenerator
from MazeGen.algo.dijkstras_solver import Dijkstras


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

    # from menu.menu import menu_loop
    # menu_loop(config)
    maze_gen = MazeGenerator(config=config, algorithm="kruskal")
    maze_gen.create_output_file()
    # maze_gen.draw_maze()
    solver = Dijkstras(config, maze_gen)
    solver.solve()


if __name__ == "__main__":
    main()
