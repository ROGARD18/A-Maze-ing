from draw_maze import draw_maze


def gen_line(line: int, maze: list[list[list]], width: int) -> None:

    line_cell: list[list] = []

    for i in range(width):

        cell: list = [0, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        else:
            if line_cell[i - 1][3] == 1:
                cell[1] = 1
        if line == 0 or maze[line-1][i][2] == 1:
            cell[0] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_first_line(width: int, maze: list[list[list]]) -> None:

    line_cell: list[list] = []

    for i in range(width):
        cell: list = [1, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        elif i == width - 1:
            cell[1] = 1
        if i != 0 and line_cell[i - 1][1] == 1:
            cell[3] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_last_line(height: int, width: int, maze: list[list[list]]) -> None:

    line_cell: list[list] = []

    for i in range(width):
        cell: list = [0, 0, 1, 0]
        if i == 0:
            cell[3] = 1
        elif i == width - 1:
            cell[1] = 1
        if maze[height-3][i][2] == 1:
            cell[0] = 1
        if i != 0 and line_cell[i - 1][1] == 1:
            cell[3] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def main() -> None:
    width: int = 4
    height: int = 4
    maze: list[list[list]] = []
    gen_first_line(width, maze)
    for i in range(height-2):
        gen_line(i, maze, width)
    gen_last_line(height, width, maze)
    for lines in maze:
        print("")
        for cell in lines:
            if cell == [0, 0, 0, 1]:
                print("1", end="")
            elif cell == [0, 0, 1, 0]:
                print("2", end="")
            elif cell == [0, 0, 1, 1]:
                print("3", end="")
            elif cell == [0, 1, 0, 1]:
                print("4", end="")
            elif cell == [0, 1, 0, 1]:
                print("5", end="")
            elif cell == [0, 1, 1, 0]:
                print("6", end="")
            elif cell == [0, 1, 1, 1]:
                print("7", end="")
            elif cell == [1, 0, 0, 0]:
                print("8", end="")
            elif cell == [1, 0, 0, 1]:
                print("9", end="")
            elif cell == [1, 0, 1, 0]:
                print("A", end="")
            elif cell == [1, 0, 1, 1]:
                print("B", end="")
            elif cell == [1, 1, 0, 0]:
                print("C", end="")
            elif cell == [1, 1, 0, 1]:
                print("D", end="")
            elif cell == [1, 1, 1, 0]:
                print("E", end="")
            elif cell == [1, 1, 1, 1]:
                print("F", end="")
            else:
                print(".", end="")
    print()
    draw_maze(maze)


if __name__ == "__main__":
    main()
