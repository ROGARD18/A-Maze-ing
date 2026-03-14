from utils.models import Config, Cell, Maze, TMaze
from MazeGen.generator import Colors

import random
import os, time


cell_with_N: tuple[str, str, str, str, str, str, str, str] = ('1', '3', '5', '7', '9', 'B', 'D', 'F')
cell_with_E: tuple[str, str, str, str, str, str, str, str] = ('2', '3', '6', '7', 'A', 'B', 'E', 'F')


class Kruskal(Maze):

    def __init__(self, config: Config, seed: float | None) -> None:
        self.config = config
        self.name = "kruskal"
        # if seed:
        #     self.seed = seed
        #     random.seed(seed)
        # else:
        #     self.seed = random.random()
        #     random.seed(self.seed)


    def init_maze(self, config: Config) -> TMaze:

        height: int = self.config.height
        width: int = self.config.width
        maze: TMaze = []
        count_id: int = 0
        for i in range(height):
            line: list[Cell] = []
            for j in range(width):
                if i == config.entry_y and j == config.entry_x:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=True,
                        is_exit=False
                    )
                elif i == config.exit_y and j == config.exit_x:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=False,
                        is_exit=True,
                    )
                else:
                    cell: Cell = Cell(
                        west=1,
                        east=1,
                        south=1,
                        north=1,
                        set_id=count_id,
                        y=i,
                        x=j,
                        is_entry=False,
                        is_exit=False,
                    )
                line.append(cell)
                count_id += 1
            maze.append(line)

        return maze

    def get_entry(self, cell: Cell) -> Cell:
        return cell

    def get_exit(self, cell: Cell) -> Cell:
        return cell
    
    def _write_maze(self, maze: TMaze) -> None:
        flag_first = True
        walls_to_char = {
            (0,0,0,0): '0', (0,0,0,1): '1', (0,0,1,0): '2', (0,0,1,1): '3',
            (0,1,0,0): '4', (0,1,0,1): '5', (0,1,1,0): '6', (0,1,1,1): '7',
            (1,0,0,0): '8', (1,0,0,1): '9', (1,0,1,0): 'A', (1,0,1,1): 'B',
            (1,1,0,0): 'C', (1,1,0,1): 'D', (1,1,1,0): 'E', (1,1,1,1): 'F',
            (-1,-1,-1,-1): ' ',
        }
        with open(self.config.output_file, "w+") as file:
            for line in maze:
                if flag_first:
                    flag_first = False
                else:
                    file.write('\n')
                for cell in line:
                    key = (cell.west, cell.south, cell.east, cell.north)
                    file.write(walls_to_char.get(key, 'F'))
    
    def draw_maze(self) -> None:

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
        color: str = colors_list[2]
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

    def generate(self, animated: bool | None) -> TMaze:

        config = self.config
        maze: TMaze = self.init_maze(self.config)
        cells_42: list[Cell] = super().make_42(config, maze)
        for cell in cells_42:
            cell.set_id = -42
        edges: list[tuple[tuple[int, int], tuple[int, int], "str"]] = []

        for x in range(config.height):
            for y in range(config.width):
                first_cell: Cell = maze[x][y]
                if first_cell in cells_42:
                    continue

                if x < config.height - 1:
                    second_cell: Cell = maze[x + 1][y]
                    if not (second_cell in cells_42):
                        edges.append(((x, y), (x + 1, y), "south"))

                if y < config.width - 1:
                    second_cell = maze[x][y + 1]
                    if not (second_cell in cells_42):
                        edges.append(((x, y), (x, y + 1), "east"))

        random.shuffle(edges)

        for (x1, y1), (x2, y2), wall in edges:
            cell_one: Cell = maze[x1][y1]
            cell_two: Cell = maze[x2][y2]

            if cell_one.set_id != cell_two.set_id:
                if wall == "south":
                    cell_one.south = 0
                    cell_two.north = 0

                elif wall == "east":
                    cell_one.east = 0
                    cell_two.west = 0

                good_id: int = cell_one.set_id
                bad_id: int = cell_two.set_id

                for line in maze:
                    for cell in line:
                        if cell.set_id == bad_id:
                            cell.set_id = good_id
                if animated:
                    self._write_maze(maze)
                    os.system('clear')
                    self.draw_maze()
                    time.sleep(0.05)

        return maze

    # def animated_generation(self) -> TMaze:
    #     config = self.config
    #     maze: TMaze = self.init_maze(self.config)
    #     cells_42: list[Cell] = super().make_42(config, maze)
    #     for cell in cells_42:
    #         cell.set_id = -42
    #     edges: list[tuple[tuple[int, int], tuple[int, int], "str"]] = []

    #     for x in range(config.height):
    #         for y in range(config.width):
    #             first_cell: Cell = maze[x][y]
    #             if first_cell in cells_42:
    #                 continue

    #             if x < config.height - 1:
    #                 second_cell: Cell = maze[x + 1][y]
    #                 if not (second_cell in cells_42):
    #                     edges.append(((x, y), (x + 1, y), "south"))

    #             if y < config.width - 1:
    #                 second_cell = maze[x][y + 1]
    #                 if not (second_cell in cells_42):
    #                     edges.append(((x, y), (x, y + 1), "east"))

    #     random.shuffle(edges)

    #     for (x1, y1), (x2, y2), wall in edges:
    #         cell_one: Cell = maze[x1][y1]
    #         cell_two: Cell = maze[x2][y2]

    #         if cell_one.set_id != cell_two.set_id:
    #             if wall == "south":
    #                 cell_one.south = 0
    #                 cell_two.north = 0

    #             elif wall == "east":
    #                 cell_one.east = 0
    #                 cell_two.west = 0

    #             good_id: int = cell_one.set_id
    #             bad_id: int = cell_two.set_id

    #             for line in maze:
    #                 for cell in line:
    #                     if cell.set_id == bad_id:
    #                         cell.set_id = good_id
    #             self._write_maze(maze)
    #             os.system('clear')
    #             self.draw_maze()
    #             time.sleep(0.05)

    #     return maze
