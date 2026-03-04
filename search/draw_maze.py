def make_line(line: str) -> str:
    line_res: str = ""
    for cell in line:
        if cell in ('1', '2', '3', '8', '9', 'A', 'B'):
            line_res += '                '
            if cell in ('9', 'A', 'B'):
                line_res += '█'
        else:
            line_res += '▄▄▄▄▄▄▄▄▄▄'
            if cell in ('C', 'D', 'E', 'F'):
                line_res += '█'
    return line_res


def print_line_col(line: str):
    for i in range(3):
        for c in line:
            (print('█', end="")
                if c == '█'
                else print(' ', end=""))
        print()


def draw_maze(file: str) -> None:
    try:
        with open(file, "r") as file:
            content: str = file.read()
    except Exception as e:
        print(e)
        return
    content_split: str = content.split('\n')
    # width: int = len(content_split[0])
    # height: int = len(content_split)
    # for line in content:
    line_res: str = make_line(content[0])
    # print(line_res)
    # print_line_col(line_res)
    for line in content.split('\n'):
        line_res = make_line(line)
        print(line_res)
        print_line_col(line_res)
    print('\n')
