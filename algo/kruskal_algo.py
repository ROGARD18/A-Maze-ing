from utils.models import Config, Maze, Cell


def gen_full_maze(config: Config) -> Maze:
    height: int = config.height
    width: int = config.width
    maze: Maze = Maze()

    line: list[Cell] = []
    for _ in range(width):
        cell: Cell = Cell(west=1, east=1, south=1, north=1)
        line.append(cell)

    for _ in range(height):
        maze.cells.append(line)


def kruskal(config: Config) -> str:
    maze: Maze = gen_full_maze(config)

    return "output_file.txt"
