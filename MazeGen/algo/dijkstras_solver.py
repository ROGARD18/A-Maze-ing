from utils.models import Cell, Config
from MazeGen.generator import MazeGenerator, Solver
from collections import deque
from math import sqrt, inf


class MinHeapPriorityQ:

    def __init__(self) -> None:
        self.queue: deque[Cell] = deque()

    def queue_front(self, cell: Cell) -> None:
        self.queue.appendleft(cell)

    def insert_cell(self, cell: Cell) -> None:
        for i, elem in enumerate(self.queue):
            if cell.root_distance < elem.root_distance:
                if i > 0:
                    self.queue.insert(i - 1, cell)
                else:
                    self.queue.appendleft(cell)
                return
        self.queue.append(cell)

    def get_max_priority_cell(self) -> Cell:
        return self.queue.popleft()

    def queue_lenght(self) -> int:
        return len(self.queue)


class Dijkstras(Solver):

    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        """
        self.maze = Grid
        Args:
            config (Config): config object
            maze (MazeGenerator): Maze object
        """
        self.entry_cell: Cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell: Cell = maze.maze[config.exit_y][config.exit_x]
        self.maze: list[list[Cell]] = maze.maze
        self.config: Config = config

    @staticmethod
    def calculate_root_distance(cell1: Cell, cell2: Cell) -> float:
        return sqrt((cell1.y - cell2.y) ** 2 + (cell1.x - cell2.x) ** 2)

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Add the cell's neighborhood to a list"""
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
        # Init distances: entry = 0, others = inf
        dist: dict[Cell, float] = {}
        prev: dict[Cell, Cell | None] = {}

        for line in self.maze:
            for cell in line:
                dist[cell] = inf
                prev[cell] = None

        dist[self.entry_cell] = 0.0
        self.entry_cell.root_distance = 0.0

        queue = MinHeapPriorityQ()
        queue.queue_front(self.entry_cell)

        visited: set[Cell] = set()

        while queue.queue_lenght() != 0:
            current: Cell = queue.get_max_priority_cell()

            # Skip if the current cell is the entry.
            if current in visited:
                continue
            visited.add(current)

            if current is self.exit_cell:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue

                # The 1 is the edge weight. 
                # Always 1 cause in our maze, every neighbors is one cell away.
                new_dist: float = dist[current] + 1

                # If the cell isnt visited yet, new dist will be less than the dist[neighbor] cause it's infinity
                # Then we insert it at the right place in the deque
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    neighbor.root_distance = new_dist
                    prev[neighbor] = current
                    queue.insert_cell(neighbor)

        # Reconstruct path from exit to entry
        path: list[Cell] = []
        current_cell: Cell | None = self.exit_cell

        # No path found
        if prev[self.exit_cell] is None and self.exit_cell is not self.entry_cell:
            return None

        while current_cell is not None:
            path.append(current_cell)
            current_cell = prev[current_cell]

        path.reverse()
        print([(cell.y, cell.x) for cell in path])
        return path