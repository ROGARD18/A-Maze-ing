from utils.models import Config,TMaze
from MazeGen.algo.kruskal_algo import Kruskal

cell_with_N: tuple[str, str, str, str, str, str, str, str] = ('1', '3', '5', '7', '9', 'B', 'D', 'F')
cell_with_E: tuple[str, str, str, str, str, str, str, str] = ('2', '3', '6', '7', 'A', 'B', 'E', 'F')


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


class Maze_Generator():

    def __init__(self, config: Config, algorithm: str) -> None:
        self.config = config
        self.algorithm = algorithm
        self.maze: TMaze = []

        if algorithm == "kruskal":
            kruskal = Kruskal(config)
            self.maze: TMaze = kruskal.generate()
        # elif algorithm == "prism":
        #     self.maze: Maze = Kruskal.generate()
        # elif algorithm == "wilson":
        #     self.maze: Maze = Kruskal.generate()

    def create_output_file(self) -> str:

        flag_first: bool = True
        file_name: str = self.config.output_file
        maze = self.maze
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

    def draw_maze(self) -> None:
        from random import choice

        def make_first_maze_line(line: str, color: str, color_end: str
                                 ) -> list[str]:
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
                    if (index == self.config.entry_y and
                     0 == self.config.entry_x):
                        line_res += (
                            f"\u001b[0;33m████{color_end}")
                    elif (index == self.config.exit_y and
                            0 == self.config.exit_x):
                        line_res += (f"\u001b[0;31m████{color_end}")
                    elif cell == 'F':
                        line_res += (f"{color}{Colors.faint}████{color_end}")
                    else:
                        line_res += '    '
                    if cell in cell_with_E:
                        line_res += f'{color}█'
                    else:
                        line_res += ' '
                    index += 1
                lines_first_cell.append(line_res)

            return lines_first_cell

        def make_first_cell_line(line: str, previous_line: str) -> str:
            line_res: str = "█"
            index: int = 0

            for cell, prev_cell in zip(line, previous_line):
                if cell in cell_with_N:
                    line_res += '▄▄▄▄'
                else:
                    line_res += '    '

                if prev_cell in cell_with_E:
                    line_res += '█'
                else:
                    line_res += '▄'
                index += 1

            return line_res

        def make_cell_middle_line(line_index: int, line: str, color: str,
                                  color_end: str) -> str:
            line_res: str = "█"
            index: int = 0
            for cell in line:
                if index == self.config.entry_y and \
                 line_index == self.config.entry_x:
                    line_res += (
                        f"\u001b[0;33m████{color_end}")
                elif index == self.config.exit_y and \
                        line_index == self.config.exit_x:
                    line_res += (
                        f"\u001b[0;31m████{color_end}")
                elif cell == 'F':
                    line_res += (f"{color}{Colors.faint}████{color_end}")
                else:
                    line_res += ('    ')
                if cell in cell_with_E:
                    line_res += (f"{color}█")
                else:
                    line_res += (' ')
                index += 1

            return line_res

        def make_last_line(line: list[str]) -> str:
            line_res: str = '█'

            for cell in line:
                line_res += '▄▄▄▄'
                if cell in cell_with_E:
                    line_res += '█'
                else:
                    line_res += '▄'
            return line_res

        # main
        t = Colors
        colors_list: list[str] = [t.yellow, t.red, t.green, t.blue, t.cyan,
                                  t.magenta, t.white]
        color: str = choice(colors_list)
        color_end: str = t.end

        # try to open output_file
        try:
            with open(self.config.output_file, "r") as file:
                content: str = file.read()
        except Exception as e:
            print(e)
            print("line: 179 generator.py")
            return

        lines = content.split('\n')
        line_index: int = 0
        # print first line of maze
        for line in make_first_maze_line(lines[0], color, color_end):
            print(f"{color}{line}{color_end}")
        first_line: str = lines[0]
        lines.remove(lines[0])

        # print interior of maze
        index: int = 0
        for line in lines:
            previous = first_line if index == 0 else lines[index - 1]
            print(f"{color}{t.bold}{make_first_cell_line(line, previous)}"
                  f"{color_end}")
            line_index += 1
            for _ in range(2):
                print(f"{color}{make_cell_middle_line(line_index, line,
                                                      color, color_end)}"
                      f"{color_end}")
            index += 1

        # print last line of maze
        print(f"{color}{make_last_line(list(lines[len(lines) - 1]))}{color_end}")
