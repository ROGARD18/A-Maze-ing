from utils.models import Cell, Config, Maze
from MazeGen.generator import MazeGenerator, Solver
from collections import deque

class PriorityQueue:

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


class Dijkstras(Solver):

    
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        self.entry_cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell = maze.maze[config.exit_y][config.exit_x]
        self.maze = maze.maze
        self.config = config

    def solve(self) -> None:

        queue = PriorityQueue()
        queue.queue_front(self.entry_cell)
        dist = []
        for y in range(self.config.height):
            for x in range(self.config.width):
                pass
