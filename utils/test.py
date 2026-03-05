from draw_maze_file import draw_maze
import sys


def gen_line(line: int, maze: list[list[list[int]]], width: int) -> None:

    line_cell: list[list[int]] = []

    for i in range(width):

        cell: list[int] = [0, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        else:
            if line_cell[i - 1][3] == 1:
                cell[1] = 1
        if line == 0 or maze[line-1][i][2] == 1:
            cell[0] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_first_line(width: int, maze: list[list[list[int]]]) -> None:

    line_cell: list[list[int]] = []

    for i in range(width):
        cell: list[int] = [1, 0, 0, 0]
        if i == 0:
            cell[3] = 1
        elif i == width - 1:
            cell[1] = 1
        if i != 0 and line_cell[i - 1][1] == 1:
            cell[3] = 1
        line_cell.append(cell)
    maze.append(line_cell)


def gen_last_line(height: int, width: int, maze: list[list[list[int]]]) -> None:

    line_cell: list[list[int]] = []

    for i in range(width):
        cell: list[int] = [0, 0, 1, 0]
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
    print(sys.argv[1])
    draw_maze(sys.argv[1])


if __name__ == "__main__":
    main()
