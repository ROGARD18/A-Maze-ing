from utils.models import Config, Cell, Maze, Grid
import os
import time

import random


class Kruskal(Maze):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.name = "kruskal"

    def init_maze(self, config: Config) -> Grid:

        height: int = self.config.height
        width: int = self.config.width
        grid: Grid = []
        count_id: int = 0
        for i in range(height):
            line: list[Cell] = []
            for j in range(width):
                if i == config.entry_y and j == config.entry_x:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=True,
                        is_exit=False
                        )
                elif i == config.exit_y and j == config.exit_x:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=False,
                        is_exit=True,
                    )
                else:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=False,
                        is_exit=False,
                    )
                line.append(cell)
                count_id += 1
            grid.append(line)

        return grid

    def get_entry(self, cell: Cell) -> Cell:
        return cell

    def get_exit(self, cell: Cell) -> Cell:
        return cell

    def generate(self, animated: bool, color: str | None, color_42: str | None,
                 gen_time: float | None) -> Grid:

        config = self.config
        grid: Grid = self.init_maze(self.config)
        cells_42: list[Cell] = super().make_42(config, grid)
        for cell in cells_42:
            cell.set_id = -42
        edges: list[tuple[tuple[int, int], tuple[int, int], "str"]] = []

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
