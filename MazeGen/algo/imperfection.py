from MazeGen.generator import MazeGenerator
from utils.models import Config, Grid, Cell

def get_neighbors(grid: Grid, cell: Cell, config: Config) -> list[Cell]:
        """Return accessible neighbors of a cell (walls = 0 means open)"""
        neighbors: list[Cell] = []
        if cell.west == 0 and cell.x > 0:
            neighbors.append(grid[cell.y][cell.x - 1])
        if cell.east == 0 and cell.x < config.width - 1:
            neighbors.append(grid[cell.y][cell.x + 1])
        if cell.north == 0 and cell.y > 0:
            neighbors.append(grid[cell.y - 1][cell.x])
        if cell.south == 0 and cell.y < config.height - 1:
            neighbors.append(grid[cell.y + 1][cell.x])
        return neighbors

def imperfect_maze(maze_gen: MazeGenerator, config: Config, path: list[Cell]) -> Grid:

    cells_42: list[Cell] = super().make_42(config, grid) # type: ignore
    edges: list[tuple[tuple[int, int], tuple[int, int], "str"]] = []
    
    for cell in path:
         neighbors: list[Cell] = get_neighbors(maze_gen.grid, cell, config)
         for cell in neighbors:

    for x in range(config.height):
        for y in range(config.width):
            first_cell: Cell = grid[x][y]
            if first_cell in cells_42:
                continue

            if x < config.height - 1:
                second_cell: Cell = grid[x + 1][y]
                if not (second_cell in cells_42):
                    edges.append(((x, y), (x + 1, y), "south"))

            if y < config.width - 1:
                second_cell = grid[x][y + 1]
                if not (second_cell in cells_42):
                    edges.append(((x, y), (x, y + 1), "east"))

    random.shuffle(edges)

    for (x1, y1), (x2, y2), wall in edges:
        cell_one: Cell = grid[x1][y1]
        cell_two: Cell = grid[x2][y2]

        if cell_one.set_id != cell_two.set_id:
            if wall == "south":
                cell_one.south = 0
                cell_two.north = 0

            elif wall == "east":
                cell_one.east = 0
                cell_two.west = 0

            good_id: int = cell_one.set_id
            bad_id: int = cell_two.set_id

            for line in grid:
                for cell in line:
                    if cell.set_id == bad_id:
                        cell.set_id = good_id
            if animated:
                from MazeGen.generator import MazeGenerator
                os.system('clear')
                MazeGenerator.draw_maze(grid, config, color,
                                        color_42, path=None)
                time.sleep(gen_time)

    return grid