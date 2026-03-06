from utils.models import Config, Maze, Cell


def gen_full_maze(config: Config) -> Maze:
    height: int = config.height
    width: int = config.width
    maze: Maze = Maze()

    for _ in range(width):
        cell: Cell = Cell(walls={'W': 1, 'S': 1, 'E': 1, 'N': 1})
