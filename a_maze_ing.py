from utils.check_dep import check_dep
from utils.parsing import parsing
from utils.models import Config, Maze
from utils.draw_42 import draw_42
from utils.create_output_file import create_output_file
from utils.init_maze import init_maze
from pydantic import ValidationError
from utils.draw_maze_file import draw_maze
from algo. kruskal_algo import kruskal
import sys


def main() -> None:
    config: Config | None = None
    try:
        print("Checking if all dependencies are installed...")
        check_dep()
        print("Deps well installed.\n")
    except Exception as e:
        print(e)
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
    try:
        maze = init_maze(config=config)
        draw_42(config, maze)
        create_output_file(maze.cells, config.output_file)
    except Exception as e:
        print(e)
        return
    # draw_maze("maze2.txt")
    draw_maze(config.output_file)


if __name__ == "__main__":
    main()
