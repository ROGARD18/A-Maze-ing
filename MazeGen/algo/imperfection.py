from MazeGen.generator import MazeGenerator
from utils.models import Config, Grid, Cell
import random


def get_neighbors(grid: Grid, cell: Cell, config: Config, path: list[Cell]) -> list[Cell]:
    neighbors: list[Cell] = []
    if cell.x > 0:
        if grid[cell.y][cell.x - 1] not in path:
            neighbors.append(grid[cell.y][cell.x - 1])
    if cell.x < config.width - 1:
        if grid[cell.y][cell.x + 1] not in path:
            neighbors.append(grid[cell.y][cell.x + 1])
    if cell.y > 0:
        if grid[cell.y - 1][cell.x] not in path:
            neighbors.append(grid[cell.y - 1][cell.x])
    if cell.y < config.height - 1:
        if grid[cell.y + 1][cell.x] not in path:
            neighbors.append(grid[cell.y + 1][cell.x])
    return neighbors


def get_all_neighbors(grid: Grid, cell: Cell, config: Config) -> list[Cell]:
    neighbors: list[Cell] = []
    if cell.x > 0:
        neighbors.append(grid[cell.y][cell.x - 1])
    if cell.x < config.width - 1:
        neighbors.append(grid[cell.y][cell.x + 1])
    if cell.y > 0:
        neighbors.append(grid[cell.y - 1][cell.x])
    if cell.y < config.height - 1:
        neighbors.append(grid[cell.y + 1][cell.x])
    return neighbors


def count_walls(cell: Cell) -> int:
    return cell.north + cell.south + cell.east + cell.west


def break_wall(cell_one: Cell, cell_two: Cell) -> None:
    if count_walls(cell_one) <= 1 or count_walls(cell_two) <= 1:
        return
    if cell_two.x == cell_one.x + 1:
        cell_one.east = 0
        cell_two.west = 0
    elif cell_two.x == cell_one.x - 1:
        cell_one.west = 0
        cell_two.east = 0
    elif cell_two.y == cell_one.y + 1:
        cell_one.south = 0
        cell_two.north = 0
    elif cell_two.y == cell_one.y - 1:
        cell_one.north = 0
        cell_two.south = 0


def wall_exists(cell_one: Cell, cell_two: Cell) -> bool:
    if count_walls(cell_one) <= 1 or count_walls(cell_two) <= 1:
        return False
    if cell_two.x == cell_one.x + 1:
        return cell_one.east == 1
    elif cell_two.x == cell_one.x - 1:
        return cell_one.west == 1
    elif cell_two.y == cell_one.y + 1:
        return cell_one.south == 1
    elif cell_two.y == cell_one.y - 1:
        return cell_one.north == 1
    return False


def imperfect_maze(maze_gen: MazeGenerator, config: Config, path: list[Cell]) -> Grid:
    if config.perfect:
        return maze_gen.grid

    grid = maze_gen.grid
    cells_42: list[Cell] = maze_gen.maze.make_42(config, grid)

    # --- Phase 1 : casser des murs entre path et ses voisins (comportement original) ---
    nb_breaks_path = len(path) // 2
    breakable_path: list[tuple[Cell, Cell]] = []

    for cell in path:
        neighbors = get_neighbors(grid, cell, config, path)
        for neighbor in neighbors:
            if neighbor not in cells_42:
                breakable_path.append((cell, neighbor))

    random.shuffle(breakable_path)
    broken = 0
    for cell_one, cell_two in breakable_path:
        if broken >= nb_breaks_path:
            break
        if wall_exists(cell_one, cell_two):
            break_wall(cell_one, cell_two)
            broken += 1

    # --- Phase 2 : casser des murs aléatoires dans toute la grille (hors cells_42) ---
    # Environ 15% des cellules de la grille pour un aspect "imparfait réaliste"
    total_cells = config.width * config.height
    nb_breaks_grid = max(1, int(total_cells * 0.15))

    breakable_grid: list[tuple[Cell, Cell]] = []
    for row in grid:
        for cell in row:
            if cell in cells_42:
                continue
            for neighbor in get_all_neighbors(grid, cell, config):
                if neighbor not in cells_42:
                    # Éviter les doublons (A,B) et (B,A)
                    if cell.x < neighbor.x or cell.y < neighbor.y:
                        breakable_grid.append((cell, neighbor))

    random.shuffle(breakable_grid)
    broken_grid = 0
    for cell_one, cell_two in breakable_grid:
        if broken_grid >= nb_breaks_grid:
            break
        if wall_exists(cell_one, cell_two):
            break_wall(cell_one, cell_two)
            broken_grid += 1

    return grid