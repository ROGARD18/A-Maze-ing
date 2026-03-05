cell_with_N: tuple = ('1', '3', '5', '7', '9', 'B', 'D', 'F')
cell_with_E: tuple = ('2', '3', '6', '7', 'A', 'B', 'E', 'F')
cell_with_S: tuple = ('4', '5', '6', '7', '', 'C', 'D', 'E', 'F')
cell_with_W: tuple = ('8', '9', 'A', 'B', 'C', 'D', 'E', 'F')


class colors:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;34m"
    blue = "\u001b[0;34m"
    magenta = "\u001b[0;35m"
    cyan = "\u001b[0;36m"
    white = "\u001b[0;37m"
    underline = "\u001b[4m"
    bold = "\u001b[1m"
    inverse = "\u001b[7m"
    end = "\u001b[0m"


def make_first_maze_line(line: str) -> list[str]:
    lines_first_cell: list[str] = []
    line_char = "▄"
    col_char = "█"

    line_res = col_char
    lines_first_cell.append("")

    return lines_first_cell


def make_line(line: str, previous_line: str) -> str:
    line_res: str = "█"
    index: int = 0

    for cell, prev_cell in zip(line, previous_line):
        # Toutes les cell avec un nord
        if cell in cell_with_N:
            line_res += '▄▄▄▄'
        else:
            line_res += '    '
        # Toutes les cell avec un est
        if prev_cell in cell_with_E:
            line_res += '█'
        else:
            line_res += '▄'
        index += 1

    return line_res


def make_line_in_cell(line: str) -> str:
    line_res: str = "█"
    for cell in line:
        line_res += ('    ')
        if cell in ('2', '3', '6', '7', 'A', 'B', 'E', 'F'):
            line_res += ('█')
        else:
            line_res += (' ')

    return line_res


def print_last_line(lines: list, color: str) -> None:
    res = "█▄▄▄"
    for _ in range(len(lines) - 1):
        res += "▄▄▄▄"
    res += "▄▄▄█"
    print(f"{color}{res}\u001b[0m")
    print()


def draw_maze(file_name: str) -> None:
    try:
        with open(file_name, "r") as file:
            content: str = file.read()
    except Exception as e:
        print(e)
        return

    lines = content.split('\n')
    # for line in make_first_maze_line(lines[0]):
    #     print(line)
    # lines.remove(lines[0])
    index: int = 0

    for line in lines:
        previous = lines[index - 1]
        t = colors
        print(f"{t.red}{t.bold}{make_line(line, previous)}{t.end}")
        # print(make_line(line, previous))
        for _ in range(2):
            print(f"{t.red}{make_line_in_cell(line)}{t.end}")
        index += 1
    print_last_line(lines, t.red)
