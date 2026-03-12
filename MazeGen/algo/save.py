class Graph:
    def __init__(self, size: int):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight: float):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight 

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data, end_vertex_data):
        start_vertex = self.vertex_data.index(start_vertex_data)
        end_vertex = self.vertex_data.index(end_vertex_data)
        distances = [float('inf')] * self.size
        predecessors = [None] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i

            if u is None or u == end_vertex:
                print(f"Breaking out of loop. Current vertex: {self.vertex_data[u]}")
                print(f"Distances: {distances}")
                break

            visited[u] = True
            print(f"Visited vertex: {self.vertex_data[u]}")

            for v in range(self.size):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v]
                    if alt < distances[v]:
                        distances[v] = alt
                        predecessors[v] = u

        return distances[end_vertex], self.get_path(predecessors, start_vertex_data, end_vertex_data)

# Example usage
g = Graph(7)
# ... (rest of the graph setup)
distance, path = g.dijkstra('D', 'F')
print(f"Path: {path}, Distance: {distance}")

###################################################################3
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
    
    def get_max_priority_cell(self) -> Cell:
        return self.queue.popleft()

    def queue_lenght(self) -> int:
        return len(self.queue)

class Dijkstras(Solver):

    
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        """
        self.maze = Grid 
        self.adj_matrix = Contain all the edges and their weight
        Args:
            config (Config): config object
            maze (MazeGenerator): Maze object
        """
        self.entry_cell = maze.maze[config.entry_y][config.entry_x]
        self.exit_cell = maze.maze[config.exit_y][config.exit_x]
        self.maze = maze.maze
        self.config = config
        self.adj_matrix = [[0] * (config.height * config.width) for _ in range(config.height * config.width)]
        self.size = config.height * config.width
        self.vertex_data = [''] * (config.height * config.width)


    def add_edge(self, u: int, v: int, weight: float):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight 

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data


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
        # Entry got dist = 0, others inf
        dist: dict[str, list[Cell]] = {str(self.entry_cell.root_distance): [self.entry_cell]}
        dist[str(self.config.width + self.config.height)] = []
        for line in self.maze:
            for cell in line:
                dist[str(inf)].append(cell)
        
        for dis, cell in dist.items():
            print(dis, cell)

        while queue.queue_lenght() != 0:
            cell = queue.get_max_priority_cell()
            # if never visited cell / not known distance
            for neighbord in self.get_neighbors(cell):
                if float(dist[cell.root_distance]) > float(dist[0]) + neighbord.root_distance:
                    cell.root

        
        self.calculate_root_distance()