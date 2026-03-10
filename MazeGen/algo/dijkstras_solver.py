from utils.models import Cell, Config, TMaze, Maze

class PriorityQueue:
    queue: list[Cell]

    @classmethod
    def add_cell(cls, cell: Cell) -> None:
        cls.queue.append(cell)

def dijkstras(config: Config, maze: Maze) -> None:
    queue = PriorityQueue()

    entry = 
    queue.add_cell()