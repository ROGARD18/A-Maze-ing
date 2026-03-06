cell_with_N: tuple = ('1', '3', '5', '7', '9', 'B', 'D', 'F')
cell_with_E: tuple = ('2', '3', '6', '7', 'A', 'B', 'E', 'F')


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
    # opacity = "\u001b[-10m"
    faint = "\u001b[2m"


def make_first_maze_line(line: str) -> list[str]:
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

    for i in range(2):
        line_res: str = '█'
        for cell in line:
            line_res += '    '
            if cell in cell_with_E:
                line_res += '█'
            else:
                line_res += ' '
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


def make_cell_middle_lines(line: str, color: str, color_end: str) -> str:
    line_res: str = "█"
    for cell in line:
        if cell == 'F':
            line_res += (f"{color}{Colors.faint}████{color_end}")
        else:
            line_res += ('    ')
        if cell in cell_with_E:
            line_res += (f"{color}█")
        else:
            line_res += (' ')

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


def draw_maze(file_name: str) -> None:
    from random import choice
    t = Colors
    colors_list: list[str] = [t.yellow, t.red, t.green, t.blue, t.cyan,
                         t.magenta, t.white]
    color: str = choice(colors_list)
    color_end: str = t.end

    # try to open output_file
    try:
        with open(file_name, "r") as file:
            content: str = file.read()
    except Exception as e:
        print(e)
        return

    lines = content.split('\n')

    # print first line of maze
    for line in make_first_maze_line(lines[0]):
        print(f"{color}{line}{color_end}")
    first_line: str = lines[0]
    lines.remove(lines[0])

    # print interior of maze
    index: int = 0
    for line in lines:
        previous = first_line if index == 0 else lines[index - 1]
        print(f"{color}{t.bold}{make_first_cell_line(line, previous)}"
              f"{color_end}")
        for _ in range(2):
            print(f"{color}{make_cell_middle_lines(line, color, color_end)}"
                  f"{color_end}")
        index += 1

    # print last line of maze
    print(f"{color}{make_last_line(lines[len(lines) - 1])}{color_end}")
