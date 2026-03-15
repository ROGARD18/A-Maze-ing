from MazeGen.generator import MazeGenerator
from utils.models import Config, Grid, Cell
import random


def get_neighbors(
    grid: Grid, cell: Cell, config: Config, path: list[Cell]
) -> list[Cell]:
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


def break_wall(cell_one: Cell, cell_two: Cell) -> None:
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


def imperfect_maze(
    maze_gen: MazeGenerator, config: Config, path: list[Cell], nb_breaks: int = 5
) -> Grid:
    if config.perfect:
        return maze_gen.grid

    grid = maze_gen.grid
    cells_42: list[Cell] = maze_gen.maze.make_42(config, grid)
    breakable: list[tuple[Cell, Cell]] = []

    for cell in path:
        neighbors = get_neighbors(grid, cell, config, path)
        for neighbor in neighbors:
            if neighbor not in cells_42:
                breakable.append((cell, neighbor))

    random.shuffle(breakable)

    broken: int = 0
    for cell_one, cell_two in breakable:
        if broken >= nb_breaks:
            break
        if _wall_exists(cell_one, cell_two):
            break_wall(cell_one, cell_two)
            broken += 1

    return grid


def _wall_exists(cell_one: Cell, cell_two: Cell) -> bool:
    if cell_two.x == cell_one.x + 1:
        return cell_one.east == 1
    elif cell_two.x == cell_one.x - 1:
        return cell_one.west == 1
    elif cell_two.y == cell_one.y + 1:
        return cell_one.south == 1
    elif cell_two.y == cell_one.y - 1:
        return cell_one.north == 1
    return False
