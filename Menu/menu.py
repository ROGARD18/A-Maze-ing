from mazegen.generator import MazeGenerator, Colors
from mazegen.models import Config, Grid, Cell
from random import choice
import subprocess


def menu_loop(config: Config) -> None:
    flag_first: bool = True
    gen_time: float = 0.05
    draw_path: bool = False

    t = Colors
    colors_list: list[str] = [t.yellow, t.green, t.blue, t.cyan, t.magenta]

    color: str = Colors.yellow
    color_42: str = Colors.magenta
    path: list[Cell] = []
    maze_gen: MazeGenerator | None = None

    def generate_maze() -> tuple[MazeGenerator, list[Cell]]:
        gen = MazeGenerator(config=config, algorithm="kruskal", color=color,
                            color_42=color_42, gen_time=gen_time)
        path_tuple = gen.solve()
        gen.make_imperfect(path_tuple[0])
        gen.solution = None
        gen.solution_str = None
        path_tuple = gen.solve()
        gen.create_output_file(path_tuple[1])
        return gen, path_tuple[0][:-1]

    while True:
        subprocess.run(["clear"], check=False)

        if flag_first:
            maze_gen, path = generate_maze()

        try:
            assert maze_gen is not None
        except AssertionError as e:
            print(e)
            return
        maze: Grid = maze_gen.grid
        subprocess.run(["clear"], check=False)
        if draw_path:
            maze_gen.draw_maze(maze, config, color, color_42, path)
        else:
            maze_gen.draw_maze(maze, config, color, color_42, None)

        flag_first = False
        print("\n\n            __        _  _   __   ____  ____      __  __ "
              "_   "
              "___ \n"
              "           / _\\  ___ ( \\/ ) / _\\ (__  )(  __) ___ (  )(  ( "
              "\\ / __)\n"
              "          /    \\(___)/ \\/ \\/    \\ / _/  ) _) (___) )( /    "
              "/( (_ \\\n"
              "          \\_/\\_/     \\_)(_/\\_/\\_/(____)(____)     (__)\\_"
              ")__) \\___/")

        print("\n                               --- MENU ---")
        print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
              "▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
        print("    █                                                          "
              "             █")
        print("    █ 1: Change walls color            5: Change width or "
              "height of maze    █")
        print("    █                                                          "
              "             █")
        print("    █ 2: Change 42 color               "
              "6: Change time maze creation"
              "         █")
        print("    █                                                          "
              "             █")
        print("    █ 3: Generate new maze         "
              "                                         █")
        print("    █                                                          "
              "             █")
        print("    █ 4: Show/Hide path (shortest)     "
              "                                     █")
        print("    █                                     "
              f"(current time: {gen_time})"
              "              █")
        print("    █ q: Exit                                                  "
              "             █")
        print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
              "▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print("")

        request = input(f"{t.yellow} --->  {t.end}")
        if request == 'q':
            break

        elif request == '1':
            new_color = choice(colors_list)
            while new_color is color:
                new_color = choice(colors_list)
            color = new_color

        elif request == '2':
            new_color_42: str = choice(colors_list)
            while new_color_42 is color:
                new_color_42 = choice(colors_list)
            color_42 = new_color_42

        elif request == '3':
            maze_gen, path = generate_maze()

        elif request == '4':
            draw_path = not draw_path

        elif request == '5':
            print("")
            print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            print("    █                          █")
            print("    █ 1: Change width  (min 9) █")
            print("    █                          █")
            print("    █ 2: Change height (min 7) █")
            print("    █                          █")
            print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\n")

            request = input(f"{t.yellow} --->  {t.end}")
            while request != '1' and request != '2':
                if ' ' in request:
                    print("No space in request !")
                else:
                    print(f"{request} is INVALID ! Need 1 OR 2")
                request = input(f"{t.yellow} --->  {t.end}")

            width: int | None = None
            height: int | None = None

            if request == '1':
                print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
                print("    █                   █")
                print("    █ ENTER NEW WIDTH:  █")
                print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
                valid: bool = False
                while not valid:
                    request = input(f"{t.yellow} --->  {t.end}")
                    try:
                        val = int(request)
                        if val < 9:
                            raise ValueError
                        width = val
                        valid = True
                    except Exception:
                        print(f"The input: {request} is not a number or"
                              " not superior to 8")

            elif request == '2':
                print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
                print("    █                   █")
                print("    █ ENTER NEW HEIGHT: █")
                print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
                valid = False
                while not valid:
                    request = input(f"{t.yellow} --->  {t.end}")
                    try:
                        val = int(request)
                        if val < 7:
                            raise ValueError
                        height = val
                        valid = True
                    except Exception:
                        print(f"The input: {request} is not a number or"
                              " not superior to 6")

            if height:
                config.height = height
                config.exit_y = height - 1
            if width:
                config.width = width
                config.exit_x = width - 1
            config.entry_x = 0
            config.entry_y = 0
            maze_gen, path = generate_maze()

        elif request == '6':
            print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            print("    █                                  █")
            print("    █ ENTER NEW Time (ex = 0.05):      █")
            print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
            valid = False
            while not valid:
                request = input(f"{t.yellow} --->  {t.end}")
                try:
                    gen_time = float(request)
                    valid = True
                except Exception:
                    print(f"The input: {request} is not a number")
