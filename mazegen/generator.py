from mazegen.models import Config, Grid, Cell
from abc import abstractmethod, ABC
import random


class Colors:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    blue = "\u001b[0;34m"
    magenta = "\u001b[0;35m"
    cyan = "\u001b[0;36m"
    white = "\u001b[0;37m"
    underline = "\u001b[4m"
    bold = "\u001b[1m"
    inverse = "\u001b[7m"
    end = "\u001b[0m"
    faint = "\u001b[2m"


class MazeGenerator:

    def __init__(
        self, config: Config, algorithm: str,
        color: str, color_42: str, gen_time: float
    ) -> None:
        self.config = config
        self.algorithm = algorithm
        self.grid: Grid = []
        self.color = color
        self.color_42 = color_42
        self.solution: list[Cell] | None = None
        self.solution_str: str | None = None

        if algorithm == "kruskal":
            from mazegen.kruskal_algo import Kruskal

            self.maze = Kruskal(config)
            self.grid = self.maze.generate(
                animated=True,
                color=color,
                color_42=color_42,
                gen_time=gen_time
            )

    def _count_walls(self, cell: Cell) -> int:
        return cell.north + cell.south + cell.east + cell.west

    def _break_wall(self, cell_one: Cell, cell_two: Cell) -> None:
        if (self._count_walls(cell_one) <= 1
                or self._count_walls(cell_two) <= 1):
            return
        if cell_two.x == cell_one.x + 1:
            cell_one.east = 0
            cell_two.west = 0
        elif cell_two.x == cell_one.x - 1:
            cell_one.west = 0
            cell_two.east = 0
        elif cell_two.y == cell_one.y + 1:
            cell_one.south = 0
            cell_two.north = 0
        elif cell_two.y == cell_one.y - 1:
            cell_one.north = 0
            cell_two.south = 0

    def _wall_exists(self, cell_one: Cell, cell_two: Cell) -> bool:
        if (self._count_walls(cell_one) <= 1
                or self._count_walls(cell_two) <= 1):
            return False
        if cell_two.x == cell_one.x + 1:
            return cell_one.east == 1
        elif cell_two.x == cell_one.x - 1:
            return cell_one.west == 1
        elif cell_two.y == cell_one.y + 1:
            return cell_one.south == 1
        elif cell_two.y == cell_one.y - 1:
            return cell_one.north == 1
        return False

    def _get_neighbors_outside_path(self,
                                    cell: Cell,
                                    path: list[Cell]) -> list[Cell]:
        neighbors: list[Cell] = []
        grid = self.grid
        config = self.config
        if cell.x > 0 and grid[cell.y][cell.x - 1] not in path:
            neighbors.append(grid[cell.y][cell.x - 1])
        if (cell.x < config.width - 1
                and grid[cell.y][cell.x + 1] not in path):
            neighbors.append(grid[cell.y][cell.x + 1])
        if cell.y > 0 and grid[cell.y - 1][cell.x] not in path:
            neighbors.append(grid[cell.y - 1][cell.x])
        if (cell.y < config.height - 1
                and grid[cell.y + 1][cell.x] not in path):
            neighbors.append(grid[cell.y + 1][cell.x])
        return neighbors

    def _get_all_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        grid = self.grid
        config = self.config
        if cell.x > 0:
            neighbors.append(grid[cell.y][cell.x - 1])
        if cell.x < config.width - 1:
            neighbors.append(grid[cell.y][cell.x + 1])
        if cell.y > 0:
            neighbors.append(grid[cell.y - 1][cell.x])
        if cell.y < config.height - 1:
            neighbors.append(grid[cell.y + 1][cell.x])
        return neighbors

    def make_imperfect(self, path: list[Cell]) -> None:
        if self.config.perfect:
            return

        config = self.config
        grid = self.grid
        cells_42: list[Cell] = self.maze.make_42(config, grid)

        nb_breaks_path = len(path) // 2
        breakable_path: list[tuple[Cell, Cell]] = []
        for cell in path:
            for neighbor in self._get_neighbors_outside_path(cell, path):
                if neighbor not in cells_42:
                    breakable_path.append((cell, neighbor))

        random.shuffle(breakable_path)
        broken = 0
        for cell_one, cell_two in breakable_path:
            if broken >= nb_breaks_path:
                break
            if self._wall_exists(cell_one, cell_two):
                self._break_wall(cell_one, cell_two)
                broken += 1

        total_cells = config.width * config.height
        nb_breaks_grid = max(1, int(total_cells * 0.05))
        breakable_grid: list[tuple[Cell, Cell]] = []
        for row in grid:
            for cell in row:
                if cell in cells_42:
                    continue
                for neighbor in self._get_all_neighbors(cell):
                    if neighbor not in cells_42:
                        if cell.x < neighbor.x or cell.y < neighbor.y:
                            breakable_grid.append((cell, neighbor))

        random.shuffle(breakable_grid)
        broken_grid = 0
        for cell_one, cell_two in breakable_grid:
            if broken_grid >= nb_breaks_grid:
                break
            if self._wall_exists(cell_one, cell_two):
                self._break_wall(cell_one, cell_two)
                broken_grid += 1

    def _get_passable_neighbors(self, cell: Cell) -> list[Cell]:
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

    def solve(self) -> tuple[list[Cell], str]:
        from collections import deque
        from math import inf

        if self.solution is not None and self.solution_str is not None:
            return (self.solution, self.solution_str)

        config = self.config
        grid = self.grid
        entry: Cell = grid[config.entry_y][config.entry_x]
        exit_cell: Cell = grid[config.exit_y][config.exit_x]

        dist: dict[Cell, float] = {}
        prev: dict[Cell, Cell | None] = {}
        for row in grid:
            for cell in row:
                dist[cell] = inf
                prev[cell] = None
        dist[entry] = 0.0

        queue: deque[Cell] = deque([entry])
        visited: set[Cell] = set()

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if current is exit_cell:
                break
            for neighbor in self._get_passable_neighbors(current):
                if neighbor in visited:
                    continue
                new_dist = dist[current] + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current
                    queue.append(neighbor)

        path: list[Cell] = []
        cur: Cell | None = exit_cell
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

        res = ""
        prev_cell = path[0]
        for i, cell in enumerate(path):
            if i == 0:
                continue
            if cell.y > prev_cell.y:
                res += "S"
            elif cell.y < prev_cell.y:
                res += "N"
            elif cell.x > prev_cell.x:
                res += "E"
            elif cell.x < prev_cell.x:
                res += "W"
            prev_cell = cell

        self.solution = path
        self.solution_str = res
        return (path, res)

    def create_output_file(self, path: str) -> str:
        flag_first: bool = True
        file_name: str = self.config.output_file
        maze = self.grid
        wall_map: dict[tuple[int, ...], str] = {
            (0, 0, 0, 0): "0",
            (0, 0, 0, 1): "1",
            (0, 0, 1, 0): "2",
            (0, 0, 1, 1): "3",
            (0, 1, 0, 0): "4",
            (0, 1, 0, 1): "5",
            (0, 1, 1, 0): "6",
            (0, 1, 1, 1): "7",
            (1, 0, 0, 0): "8",
            (1, 0, 0, 1): "9",
            (1, 0, 1, 0): "A",
            (1, 0, 1, 1): "B",
            (1, 1, 0, 0): "C",
            (1, 1, 0, 1): "D",
            (1, 1, 1, 0): "E",
            (1, 1, 1, 1): "F",
            (-1, -1, -1, -1): " ",
        }
        with open(file_name, "w+") as file:
            for line in maze:
                if flag_first:
                    flag_first = False
                else:
                    file.write("\n")
                for cell in line:
                    key = (cell.west, cell.south, cell.east, cell.north)
                    file.write(wall_map.get(key, "?"))
            print("\n", file=file)
            print(f"{self.config.entry_x},{self.config.entry_y}", file=file)
            print(f"{self.config.exit_x},{self.config.exit_y}", file=file)
            print(path, file=file, end="")
        return file_name

    @staticmethod
    def draw_maze(
        maze: Grid,
        config: Config,
        color: str,
        color_42: str,
        path: list[Cell] | None
    ) -> None:

        def make_first_maze_line(
            line: list[Cell],
            color: str,
            color_end: str,
            color_42: str,
            path: list[Cell] | None,
            config: Config,
        ) -> list[str]:
            lines_first_cell: list[str] = []
            line_res: str = "▄"
            for cell in line:
                line_res += "▄▄▄▄▄"
            lines_first_cell.append(line_res)
            for _ in range(2):
                line_res = "█"
                index: int = 0
                for cell in line:
                    if index == config.entry_x and 0 == config.entry_y:
                        line_res += f"\u001b[0;33m████{color_end}"
                    elif path and cell in path:
                        line_res += f"\u001b[0;37m████{color_end}"
                    elif index == config.exit_x and 0 == config.exit_y:
                        line_res += f"\u001b[0;31m████{color_end}"
                    elif (
                        cell.west == 1
                        and cell.east == 1
                        and cell.south == 1
                        and cell.north == 1
                    ):
                        line_res += f"{color_42}████{color_end}"
                    else:
                        line_res += "    "
                    if cell.east == 1:
                        line_res += f"{color}█"
                    elif path and cell in path and line[index + 1] in path:
                        line_res += f"{Colors.white}█{Colors.end}"
                    else:
                        line_res += " "
                    index += 1
                lines_first_cell.append(line_res)
            return lines_first_cell

        def make_first_cell_line(
            line: list[Cell],
            previous_line: list[Cell],
            path: list[Cell] | None,
            color: str,
        ) -> str:
            line_res: str = f"{color}█{Colors.end}"
            index: int = 0
            for cell, prev_cell in zip(line, previous_line):
                if cell.north == 1:
                    line_res += f"{color}▄▄▄▄{Colors.end}"
                elif path and cell in path and prev_cell in path:
                    line_res += f"{Colors.white}████{Colors.end}"
                else:
                    line_res += "    "
                if prev_cell.east == 1:
                    line_res += f"{color}█{Colors.end}"
                elif (prev_cell.east == 0 and cell.east == 0
                        and cell.north == 0):
                    line_res += " "
                else:
                    line_res += f"{color}▄{Colors.end}"
                index += 1
            return line_res

        def make_cell_middle_line(
            line_index: int,
            line: list[Cell],
            color: str,
            color_42: str,
            path: list[Cell] | None,
        ) -> str:
            line_res: str = "█"
            index: int = 0
            for cell in line:
                if index == config.entry_x and line_index == config.entry_y:
                    line_res += f"\u001b[0;33m████{color_end}"
                elif path and cell in path:
                    line_res += f"\u001b[0;37m████{color_end}"
                elif index == config.exit_x and line_index == config.exit_y:
                    line_res += f"\u001b[0;31m████{color_end}"
                elif (
                    cell.west == 1
                    and cell.east == 1
                    and cell.south == 1
                    and cell.north == 1
                ):
                    line_res += f"{color_42}████{color_end}"
                else:
                    line_res += "    "
                if cell.east == 1:
                    line_res += f"{color}█"
                elif path and cell in path and line[index + 1] in path:
                    line_res += f"{Colors.white}█{Colors.end}"
                else:
                    line_res += " "
                index += 1
            return line_res

        def make_last_line(line: list[Cell]) -> str:
            line_res: str = "█"
            for cell in line:
                line_res += "▄▄▄▄"
                if cell.east == 1:
                    line_res += "█"
                else:
                    line_res += "▄"
            return line_res

        color_end: str = "\u001b[0m"
        line_index: int = 0

        for line_ in make_first_maze_line(
            maze[0], color, color_end, color_42, path=path, config=config
        ):
            print(f"{color}{line_}{color_end}")

        index: int = 0
        for line in maze:
            if index == 0:
                index += 1
                continue
            previous = maze[index - 1]
            print(make_first_cell_line(line, previous, path, color))
            line_index += 1
            for _ in range(2):
                print(f"{color}", end="")
                print(
                    make_cell_middle_line(line_index,
                                          line,
                                          color,
                                          color_42,
                                          path=path),
                    end="",
                )
                print(f"{color_end}")
            index += 1

        print(f"{color}{make_last_line(list(maze[len(maze) - 1]))}{color_end}")


class Solver(ABC):
    @abstractmethod
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        pass

    @abstractmethod
    def solve(self, is_new_maze: bool) -> tuple[list[Cell], str]:
        pass
