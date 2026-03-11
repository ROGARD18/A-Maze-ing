from utils.models import Cell, Config, Maze
from MazeGen.generator import MazeGenerator, Solver


class PriorityQueue:

    def __init__(self) -> None:
        self.queue: list[Cell] = []

    def add_cell(self, cell: Cell) -> None:
        self.queue.append(cell)


class Dijkstras(Solver):

    
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        self.entry_cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell = maze.maze[config.exit_y][config.exit_x]
        self.maze = maze.maze
        self.config = config

    def solve(self) -> None:

        queue = PriorityQueue()
        queue.add_cell(self.entry_cell)
        dist = []
        for y in range(self.config.height):
            for x in range(self.config.width):
                pass
