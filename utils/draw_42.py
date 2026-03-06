from utils.models import Config, Maze, Cell
# from utils.create_output_file import create_output_file

def forty_two_cell(cells: list[Cell]) -> None:
    for cell in cells:
        cell.east = 1
        cell.west = 1
        cell.south = 1
        cell.north = 1
        cell.set_id = -42

def draw_42(config: Config, maze: Maze):
    width = config.width
    height = config.height
    list_42s: list[Cell] = []
    # The 4 of 42
    list_42s.append(maze.cells[height // 2][width // 2 - 1])
    list_42s.append(maze.cells[height // 2][width // 2 - 2])
    list_42s.append(maze.cells[height // 2][width // 2 - 3])
    list_42s.append(maze.cells[height // 2 - 1][width // 2 - 3])
    list_42s.append(maze.cells[height // 2 - 2][width // 2 - 3])

    list_42s.append(maze.cells[height // 2 + 1][width // 2 - 1])
    list_42s.append(maze.cells[height // 2 + 2][width // 2 - 1])
    forty_two_cell(list_42s)