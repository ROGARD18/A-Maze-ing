from utils.models import Cell


def create_output_file(maze_cells: list[list[Cell]], file_name: str) -> str:

    flag_first: bool = True
    with open(file_name, "w+") as file:
        for line in maze_cells:
            if flag_first:
                flag_first = False
            else:
                file.write('\n')
            for cell in line:
                cell_walls: list = [cell.west, cell.south,
                                    cell.east, cell.north]
                if cell_walls == [0, 0, 0, 1]:
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

    return file_name
