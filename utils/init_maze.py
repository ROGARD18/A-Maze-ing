from utils.models import Config, Maze, Cell


def init_maze(config: Config) -> Maze:

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
            count_id += 1
        maze.cells.append(line)

    return maze
