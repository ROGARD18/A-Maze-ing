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
        self.entry_cell: Cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell: Cell = maze.maze[config.exit_y][config.exit_x]
        self.maze: list[list[Cell]] = maze.maze
        self.config: Config = config

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Return accessible neighbors of a cell (walls = 0 means open)"""
        neighbors: list[Cell] = []
        if cell.west == 0 and cell.x > 0:
            neighbors.append(self.maze[cell.y][cell.x - 1])
        if cell.east == 0 and cell.x < self.config.width - 1:
            neighbors.append(self.maze[cell.y][cell.x + 1])
        if cell.north == 0 and cell.y > 0:
            neighbors.append(self.maze[cell.y - 1][cell.x])
        if cell.south == 0 and cell.y < self.config.height - 1:
            neighbors.append(self.maze[cell.y + 1][cell.x])
        return neighbors

    def solve(self) -> list[Cell] | None:
        dist: dict[Cell, float] = {}
        prev: dict[Cell, Cell | None] = {}

        for row in self.maze:
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

        if prev[self.exit_cell] is None and self.exit_cell is not self.entry_cell:
            return None

        path: list[Cell] = []
        current_cell: Cell | None = self.exit_cell
        while current_cell is not None:
            path.append(current_cell)
            current_cell = prev[current_cell]

        print([(cell.y, cell.x) for cell in path])
        path.reverse()
        return path