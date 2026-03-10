from utils.models import Cell, Config, Maze
from MazeGen.generator import Maze_Generator, Solver


class PriorityQueue:
    queue: list[Cell]

    @classmethod
    def add_cell(cls, cell: Cell) -> None:
        cls.queue.append(cell)


class Dijkstras(Solver):
    def __init__(self, config: Config, maze: Maze_Generator) -> None:
        self.entry_cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell = maze.maze[config.exit_y][config.exit_x]


    def solve(self, config: Config, maze: Maze) -> None:
        pass

        # queue.add_cell()