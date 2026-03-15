from utils.models import Cell, Config
from MazeGen.generator import MazeGenerator, Solver
from collections import deque
from math import inf


class Dijkstras(Solver):

    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        """
        Args:
            config (Config): config object
            maze (MazeGenerator): Maze object
        """
        self.entry_cell: Cell = maze.grid[config.entry_y][config.entry_x]
        self.exit_cell: Cell = maze.grid[config.exit_y][config.exit_x]
        self.grid: list[list[Cell]] = maze.grid
        self.config: Config = config

        # print(self.entry_cell.set_id)`
        # print(self.exit_cell.set_id)`

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Return accessible neighbors of a cell (walls = 0 means open)"""
        neighbors: list[Cell] = []
        if cell.west == 0 and cell.x > 0:
            neighbors.append(self.grid[cell.y][cell.x - 1])
        if cell.east == 0 and cell.x < self.config.width - 1:
            neighbors.append(self.grid[cell.y][cell.x + 1])
        if cell.north == 0 and cell.y > 0:
            neighbors.append(self.grid[cell.y - 1][cell.x])
        if cell.south == 0 and cell.y < self.config.height - 1:
            neighbors.append(self.grid[cell.y + 1][cell.x])
        return neighbors

    def solve(self, is_new_maze: bool) -> list[Cell]:
        dist: dict[Cell, float] = {}
        prev: dict[Cell, Cell | None] = {}

        for row in self.grid:
            for cell in row:
                dist[cell] = inf
                prev[cell] = None

        dist[self.entry_cell] = 0.0

        queue: deque[Cell] = deque([self.entry_cell])
        visited: set[Cell] = set()

        while queue:
            current: Cell = queue.popleft()

            if current in visited:
                continue
            visited.add(current)

            if current is self.exit_cell:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue

                new_dist: float = dist[current] + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current
                    queue.append(neighbor)

        path: list[Cell] = []
        current_cell: Cell | None = self.exit_cell
        while current_cell is not None:
            path.append(current_cell)
            current_cell = prev[current_cell]

        path.reverse()
        res: str = ""
        for i, cell in enumerate(path):
            if i == 0:
                prev_cell = cell
                continue
            if cell.y > prev_cell.y:
                res += "S"
                prev_cell = cell
            elif cell.y < prev_cell.y:
                res += "N"
                prev_cell = cell
            elif cell.x > prev_cell.x:
                res += "E"
                prev_cell = cell
            elif cell.x < prev_cell.x:
                res += "W"
                prev_cell = cell
        if is_new_maze:
            with open(self.config.output_file, "a") as file:
                print(res, file=file, end="")
        return path
