from utils.models import Config, Maze, Cell, Algorithm
import random


class Kruskal(Algorithm):

    def __init__(self, config: Config) -> None:
        self.config = config
        self.name = "kruskal"

    def init_maze(self) -> Maze:

        height: int = self.config.height
        width: int = self.config.width
        maze: Maze = []
        count_id: int = 0
        for _ in range(height):
            line: list[Cell] = []
            for _ in range(width):
                cell: Cell = Cell(west=1, east=1, south=1,
                                  north=1, set_id=count_id)
                line.append(cell)
                count_id += 1
            maze.append(line)

        return maze

    def generate(self) -> Maze:

        config = self.config
        maze: Maze = self.init_maze()
        cells_42: list[Cell] = super().make_42(config, maze)
        for cell in cells_42:
            cell.set_id = -42
        edges: list[tuple[tuple[int, int], tuple[int, int], 'str']] = []

        for x in range(config.height):
            for y in range(config.width):
                first_cell: Cell = maze[x][y]
                if (first_cell in cells_42):
                    continue

                if x < config.height - 1:
                    seconf_cell: Cell = maze[x + 1][y]
                    if not (seconf_cell in cells_42):
                        edges.append(((x, y), (x + 1, y), 'south'))

                if y < config.width - 1:
                    seconf_cell = maze[x][y + 1]
                    if not (seconf_cell in cells_42):
                        edges.append(((x, y), (x, y + 1), 'east'))

        random.shuffle(edges)

        for (x1, y1), (x2, y2), wall in edges:
            cell_one: Cell = maze[x1][y1]
            cell_two: Cell = maze[x2][y2]

            if cell_one.set_id != cell_two.set_id:
                if wall == 'south':
                    cell_one.south = 0
                    cell_two.north = 0

                elif wall == 'east':
                    cell_one.east = 0
                    cell_two.west = 0

                good_id: int = cell_one.set_id
                bad_id: int = cell_two.set_id

                for line in maze:
                    for cell in line:
                        if cell.set_id == bad_id:
                            cell.set_id = good_id

        return maze
