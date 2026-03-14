from utils.models import Config, Grid, Cell, Grid
from MazeGen.algo.kruskal_algo import Kruskal

from abc import abstractmethod, ABC


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


class MazeGenerator():

    def __init__(self, config: Config, algorithm: str, color: str, color_42: str, gen_time: float) -> None:
        self.config = config
        self.algorithm = algorithm
        self.grid: Grid = []
        self.color = color
        self.color_42 = color_42

        if algorithm == "kruskal":
            self.maze = Kruskal(config)
            self.grid: Grid =  self.maze.generate(animated=True, color=color, color_42=color_42, gen_time=gen_time)
        # elif algorithm == "prism":
        #     self.grid: Maze = Kruskal.generate()
        # elif algorithm == "wilson":
        #     self.grid: Maze = Kruskal.generate()

    def create_output_file(self) -> str:

        flag_first: bool = True
        file_name: str = self.config.output_file
        maze = self.grid
        with open(file_name, "w+") as file:
            for line in maze:
                if flag_first:
                    flag_first = False
                else:
                    file.write('\n')
                for cell in line:
                    cell_walls: list[int] = [cell.west, cell.south,
                                             cell.east, cell.north]
                    if cell_walls == [0, 0, 0, 0]:
                        file.write('0')
                    elif cell_walls == [0, 0, 0, 1]:
                        file.write('1')
                    elif cell_walls == [0, 0, 1, 0]:
                        file.write('2')
                    elif cell_walls == [0, 0, 1, 1]:
                        file.write('3')
                    elif cell_walls == [0, 1, 0, 0]:
                        file.write('4')
                    elif cell_walls == [0, 1, 0, 1]:
                        file.write('5')
                    elif cell_walls == [0, 1, 1, 0]:
                        file.write('6')
                    elif cell_walls == [0, 1, 1, 1]:
                        file.write('7')
                    elif cell_walls == [1, 0, 0, 0]:
                        file.write('8')
                    elif cell_walls == [1, 0, 0, 1]:
                        file.write('9')
                    elif cell_walls == [1, 0, 1, 0]:
                        file.write('A')
                    elif cell_walls == [1, 0, 1, 1]:
                        file.write('B')
                    elif cell_walls == [1, 1, 0, 0]:
                        file.write('C')
                    elif cell_walls == [1, 1, 0, 1]:
                        file.write('D')
                    elif cell_walls == [1, 1, 1, 0]:
                        file.write('E')
                    elif cell_walls == [1, 1, 1, 1]:
                        file.write('F')
                    elif cell_walls == [-1, -1, -1, -1]:
                        file.write(' ')

        return file_name

    @staticmethod
    def draw_maze(maze: Grid, config: Config, color: str, color_42: str, path: list[Cell] | None
                  ) -> None:

        def make_first_maze_line(line: str, color: str, color_end: str,
                                 color_42: str, path: list[Cell] | None,
                                 config: Config) -> list[str]:
            """
            Use to create the first cell line of maze.
            Args:
                line (str): First line in maze.txt
            Returns:
                list[str]: All lines to create first cell line of maze.
            """
            lines_first_cell: list[str] = []

            line_res: str = '▄'
            for cell in line:
                line_res += '▄▄▄▄▄'
            lines_first_cell.append(line_res)

            for _ in range(2):
                line_res: str = '█'
                index: int = 0
                for cell in line:
                    if (index == config.entry_x and
                       0 == config.entry_y):
                        line_res += (
                            f"\u001b[0;33m████{color_end}")
                    elif path and cell in path:
                        line_res += (f"\u001b[0;37m████{color_end}")

                    elif (index == config.exit_x and
                            0 == config.exit_y):
                        line_res += (f"\u001b[0;31m████{color_end}")
                    elif (cell.west == 1 and cell.east == 1 and cell.south == 1
                            and cell.north == 1):
                        line_res += (f"{color_42}████{color_end}")
                    else:
                        line_res += '    '
                    if cell.east == 1:
                        line_res += f'{color}█'
                    elif path and cell in path and line[index + 1] in path:
                        line_res += f'{Colors.white}█{Colors.end}'

                    else:
                        line_res += ' '
                    index += 1
                lines_first_cell.append(line_res)

            return lines_first_cell

        def make_first_cell_line(line: str, previous_line: str,
                                 path: list[Cell] | None, color: str) -> str:
            line_res: str = f"{color}█{Colors.end}"
            index: int = 0

            for cell, prev_cell in zip(line, previous_line):
                if cell.north == 1:
                    line_res += f'{color}▄▄▄▄{Colors.end}'
                elif path and cell in path and prev_cell in path:
                    line_res += f"{Colors.white}████{Colors.end}"
                else:
                    line_res += '    '

                if prev_cell.east == 1:
                    line_res += f'{color}█{Colors.end}'
                # elif path and cell in path:
                #     line_res += f"{Colors.white}█{Colors.end}"
                else:
                    line_res += f'{color}▄{Colors.end}'
                index += 1

            return line_res

        def make_cell_middle_line(line_index: int, line: str, color: str,
                                  color_42: str, path: list[Cell]) -> str:
            line_res: str = "█"
            index: int = 0

            for cell in line:
                if index == config.entry_x and \
                 line_index == config.entry_y:
                    line_res += (
                        f"\u001b[0;33m████{color_end}")
                elif path and cell in path:
                    line_res += (f"\u001b[0;37m████{color_end}")

                elif index == config.exit_x and \
                        line_index == config.exit_y:
                    line_res += (
                        f"\u001b[0;31m████{color_end}")

                elif (cell.west == 1 and cell.east == 1 and cell.south == 1
                        and cell.north == 1):
                    line_res += (f"{color_42}████{color_end}")
                else:
                    line_res += ('    ')
                if cell.east == 1:
                    line_res += (f"{color}█")

                elif path and cell in path and line[index + 1] in path:
                    line_res += (f"{Colors.white}█{Colors.end}")
                else:
                    line_res += (' ')
                index += 1

            return line_res

        def make_last_line(line: list[str]) -> str:
            line_res: str = '█'

            for cell in line:
                line_res += '▄▄▄▄'
                if cell.east == 1:
                    line_res += '█'
                else:
                    line_res += '▄'
            return line_res

        # main
        color_end: str = "\u001b[0m"

        line_index: int = 0
        # print first line of maze
        # print("len of maze in draw_maze:", len(maze))

        
        for line in make_first_maze_line(maze[0], color, color_end,
                                         color_42, path=path, config=config):
            print(f"{color}{line}{color_end}")
        first_line: str = maze[0]

        # print interior of maze
        index: int = 0
        for line in maze:
            if index == 0:
                index += 1
                continue
            previous = first_line if index == 0 else maze[index - 1]
            print(f"{make_first_cell_line(line, previous, path, color)}")
            line_index += 1
            for _ in range(2):
                print(f"{color}"
                      f"{make_cell_middle_line(line_index, line,
                                               color, color_42, path=path)}"
                      f"{color_end}")
            index += 1

        # print last line of maze
        print(f"{color}{make_last_line(list(maze[len(maze) - 1]))}{color_end}")


class Solver(ABC):
    @abstractmethod
    def __init__(self, config: Config, maze: MazeGenerator) -> None:
        pass

    def solver(self, maze: MazeGenerator) -> None:
        pass
