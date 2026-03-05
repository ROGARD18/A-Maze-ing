def make_first_maze_line(line: str) -> list[str]:
    lines_first_cell: list[str] = []
    line_char = "▄"
    col_char = "█"

    line_res = col_char
    lines_first_cell.append("")

    return lines_first_cell


def make_line(line: str, previous_line: str | None) -> str:
    line_res: str = "█"
    index: int = 0

    for cell in line:
        if cell in ('1', '3', '5', '7', '9', 'B', 'D', 'F'):
            line_res += '▄▄▄▄'
        else:
            line_res += '    '
        if cell in ('2', '3', '6', '7', 'A', 'B', 'E', 'F'):
            if previous_line and previous_line[index] in ('4', '5', '6', '7', 'C', 'D', 'E', 'F'):
                line_res += '█'
            else:
                line_res += '█'
        else:
            line_res += ' '
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


def draw_maze(file_name: str) -> None:
    try:
        with open(file_name, "r") as file:
            content: str = file.read()
    except Exception as e:
        print(e)
        return

    lines = content.split('\n')
    for line in make_first_maze_line(lines[0]):
        print(line)
    # lines.remove(lines[0])
    index: int = 0

    for line in lines:
        index += 1
        if index > 1:
            previous = lines[index - 2]
        else:
            previous = None
        print(make_line(line, previous))
        for _ in range(2):
            print(make_line_in_cell(line))
    res = "█▄▄▄"
    for _ in range(len(lines) - 1):
        res += "▄▄▄▄"
    res += "▄▄▄█"
    print(res)
    print()
