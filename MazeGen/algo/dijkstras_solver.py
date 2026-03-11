from utils.models import Cell, Config
from MazeGen.generator import MazeGenerator, Solver
from collections import deque
from math import sqrt


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
    
    def get_max_priority_cell(self) -> Cell:
        return self.queue.popleft()

    def queue_lenght(self) -> int:
        return len(self.queue)

class Dijkstras(Solver):

    
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        self.entry_cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell = maze.maze[config.exit_y][config.exit_x]
        self.maze = maze.maze
        self.config = config


    def calculate_root_distance(self) -> None:
        for line in self.maze:
            for cell in line:
                if cell is not self.entry_cell:
                    cell.root_distance = sqrt(
                        (self.entry_cell.y - cell.y)**2 +
                        (self.entry_cell.x - cell.x)**2)

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Add the cell's neighborhood to a list
        """
        neighbors: list[Cell] = []
        if cell.west == 0:
            neighbors.append(self.maze[cell.y][cell.x - 1])
        elif cell.east == 0:
            neighbors.append(self.maze[cell.y][cell.x + 1])
        elif cell.north == 0:
            neighbors.append(self.maze[cell.y - 1][cell.x])
        elif cell.south == 0:
            neighbors.append(self.maze[cell.y + 1][cell.x - 1])
        
        return neighbors


    def solve(self) -> None:

        queue = MinHeapPriorityQ()
        # add entry cell to the PQ
        queue.queue_front(self.entry_cell)
        # add all cells to dist
        # Entry got dist = 0, others width + height (not ppossible value (infinity) not known yet)
        dist: dict[str, list[Cell]] = {str(self.entry_cell.root_distance): [self.entry_cell]}
        dist[str(self.config.width + self.config.height)] = []
        for line in self.maze:
            for cell in line:
                dist[str(self.config.width + self.config.height)].append(cell)
        
        for dis, cell in dist.items():
            print(dis, cell)

        while queue.queue_lenght() != 0:
            cell = queue.get_max_priority_cell()
            # if never visited cell / not known distance
            for neighbord in self.get_neighbors(cell):
                if float(dist[cell.root_distance]) > float(dist[0]) + neighbord.root_distance:
                    cell.root

        
        self.calculate_root_distance()