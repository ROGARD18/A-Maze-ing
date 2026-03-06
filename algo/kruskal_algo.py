from utils.models import Config, Maze, Cell
import random


# def kruskal(config: Config, maze: Maze) -> Maze:

#     entrx_y: int = config.entrx_y
#     entrx_x: int = config.entrx_x

#     eyit_y: int = config.eyit_y
#     eyit_x: int = config.eyit_x


#     finish: bool = False
#     indey: int = 0
#     while not finish:

#         walls: list = ['west', 'south', 'north', 'east']
#         y: int = random.randint(0, config.height - 1)
#         x: int = random.randint(0, config.width - 1)
#         cell_selec: Cell = maze.cells[y][x]

#         while cell_selec.set_id == -42:
#             y: int = random.randint(0, config.height - 1)
#             x: int = random.randint(0, config.width - 1)
#             cell_selec: Cell = maze.cells[y][x]

#         if x == config.height - 1:
#             walls.remove('east')

#         wall_selected: str = random.choice(walls)
#         if wall_selected == 'west':
#             print('west')
#             cell_selec.west = 0
#         elif wall_selected == 'east':
#             print('east')
#             cell_selec.east = 0
#         elif wall_selected == 'south':
#             print('south')
#             cell_selec.south = 0
#         elif wall_selected == 'north':
#             print('north')
#             cell_selec.north = 0
#         print(cell_selec)
#         print(maze.cells[config.height - 1][config.width - 1])

#         # if maze[entrx_y][entrx_x].set_id == maze[eyit_y][eyit_x]
#         indey += 1
#         if indey == 30:
#             finish = True

#     return maze


def kruskal(config: Config, maze: Maze, cells_42: list[Cell]) -> Maze:

    edges: list[tuple[tuple[int, int], tuple[int, int], 'str']] = []

    for x in range(config.height):
        for y in range(config.width):
            first_cell: Cell = maze.cells[x][y]
            if (first_cell in cells_42):
                continue

            if x < config.height - 1:
                seconf_cell: Cell = maze.cells[x + 1][y]
                if not (seconf_cell in cells_42):
                    edges.append(((x, y), (x + 1, y), 'south'))

            if y < config.width - 1:
                seconf_cell = maze.cells[x][y + 1]
                if not (seconf_cell in cells_42):
                    edges.append(((x, y), (x, y + 1), 'east'))

    random.shuffle(edges)

    for (x1, y1), (x2, y2), wall in edges:
        cell_one: Cell = maze.cells[x1][y1]
        cell_two: Cell = maze.cells[x2][y2]

        if cell_one.set_id != cell_two.set_id:
            if wall == 'south':
                cell_one.south = 0
                cell_two.north = 0

            elif wall == 'east':
                cell_one.east = 0
                cell_two.west = 0

            good_id: str = cell_one.set_id
            bad_id: str = cell_two.set_id

            for line in maze.cells:
                for cell in line:
                    if cell.set_id == bad_id:
                        cell.set_id = good_id

    return maze
