from utils.models import Config, Maze, Cell
from utils.create_output_file import create_output_file


def gen_full_maze(config: Config) -> Maze:
    height: int = config.height
    width: int = config.width

    count_id: int = 0
    maze: Maze = Maze(cells=[])
    for _ in range(height):
        line: list[Cell] = []
        for _ in range(width):
            cell: Cell = Cell(west=1, east=1, south=1,
                              north=1, set_id=count_id)
            line.append(cell)

        maze.cells.append(line)
        count_id += 1

    return maze


def kruskal(config: Config) -> None:
    maze: Maze = gen_full_maze(config)
    create_output_file(maze.cells, config.output_file)

