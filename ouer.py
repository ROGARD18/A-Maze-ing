def draw_cell(cell: str) -> None:
    if cell == '1':
        print("   ", end="")
    elif cell == '2':
        print("  █", end="")
    elif cell == '3':
        print("  █", end="")
    elif cell == '4':
        print("▄▄▄", end="")
    elif cell == '5':
        print("▄▄▄", end="")
    elif cell == '6':
        print("▄▄█", end="")
    elif cell == '7':
        print("▄▄█", end="")
    elif cell == '8':
        print("█  ", end="")
    elif cell == '9':
        print("█  ", end="")
    elif cell == 'A':
        print("█ █", end="")
    elif cell == 'B':
        print("█ █", end="")
    elif cell == 'C':
        print("█▄▄", end="")
    elif cell == 'D':
        print("█▄▄", end="")
    elif cell == 'E':
        print("█▄█", end="")
    elif cell == 'F':
        print('█▄▄█', end="")
    else:
        print("", end="")


# def isvalid_line(cell: str) -> bool:
#     return (True
#             if cell == '1' or '3' or '5' or '7' or '9' or '11' or '13' or '15'
#             else False)


# def isvalid_est(cell: str) -> bool:
#     return (True
#             if cell == '8' or '9' or '10' or '11' or '12' or '13' or '14' or
#             '15'
#             else False)


# def isvalid_west(cell: str) -> bool:
#     return (True
#             if cell == '2' or '3' or '6' or '7' or '10' or '11' or '14' or
#             '15'
#             else False)


# def draw_lines(content: str, n: int) -> None:
#     line: str = content.split("\n")[n]
#     for cell in line:
#         if isvalid_line(cell):
#             print("▄▄▄▄▄", end="")
#         else:
#             print("    ", end="")


# def draw_columns(content: str, n: int) -> None:
#     line: str = content.split("\n")[n]
#     for cell in line:
#         if isvalid_est(cell) and isvalid_west(cell):
#             print("█   █", end="")
#         elif isvalid_est(cell):
#             print("█   ",  end="")
#         elif isvalid_west(cell):
#             print("   █",  end="")
#         # elif isvalid
#         else:
#             print("    ",  end="")
#     print()
#     for cell in line:
#         if isvalid_est(cell) and isvalid_west(cell):
#             print("█   █", end="")
#         elif isvalid_est(cell):
#             print("█   ",  end="")
#         elif isvalid_west(cell):
#             print("   █",  end="")
#         else:
#             print("    ",  end="")


def count_line_size(line: str) -> int:
    i: int = 0
    for char in line:
        i += 1
    return i


def draw_maze(file: str) -> None:
    corners = {
            '9': '┌', '3': '┐',
            '12': '└', '6': '┘',
    }
    try:
        with open(file, "r") as file:
            content: str = file.read()
    except Exception as e:
        print(e)
        return
    line_0: str = content.split('\n')
    for cell in line_0:
        draw_cell(cell)
    print()
    # size: int = len(line_0)
    # line_size: int = count_line_size(line_0)
    # index: int = 1
    for line in content.split('\n'):
        for cell in line:
            draw_cell(cell)
        print()
