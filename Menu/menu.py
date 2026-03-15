from MazeGen.generator import MazeGenerator
from utils.models import Config, Grid
from random import choice
from MazeGen.algo.dijkstras_solver import Dijkstras
import os
from MazeGen.generator import Colors


def menu_loop(config: Config) -> None:
    flag_first: bool = True
    gen_time: float = 0.05
    draw_path: bool = False

    t = Colors
    colors_list: list[str] = [t.yellow, t.green, t.blue, t.cyan,
                              t.magenta]

    color: str = Colors.yellow
    color_42: str = Colors.magenta
    path = None

    while True:
        os.system('clear')

        if flag_first:
            try:
                maze_gen = MazeGenerator(config=config,
                                         algorithm="kruskal",
                                         color=color,
                                         color_42=color_42,
                                         gen_time=gen_time)

                maze_gen.create_output_file()
            except Exception as e:
                print(e)
                print("Erreur in menu_loop in flag_first")
                return
            solver = Dijkstras(config, maze_gen)
            path = solver.solve(is_new_maze=True)
            path = path[:-1]
        maze: Grid = maze_gen.grid
        if not flag_first:
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
        print("    █ 2: Change 42 color               6: Change seed          "
              "             █")
        print("    █                                                          "
              "             █")
        print("    █ 3: Generate new maze             7: Change algo          "
              "             █")
        print("    █                                                          "
              "             █")
        print("    █ 4: Show/Hide path (shortest)     "
              "8: Change time maze creation"
              "         █")
        print("    █                                     "
              f"(current time: {gen_time})"
              "              █")
        print("    █ q: Exit                                                  "
              "             █")
        print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
              "▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print("")

        request: str = input(f"{t.yellow} --->  {t.end}")
        if request == 'q':
            break

        elif request == '1':
            new_color = choice(colors_list)
            while new_color is color:
                new_color: str = choice(colors_list)
            color = new_color

        elif request == '2':
            new_color_42: str = choice(colors_list)
            while new_color_42 is color:
                new_color_42 = choice(colors_list)
            color_42 = new_color_42

        elif request == '3':
            maze_gen = MazeGenerator(config=config, algorithm="kruskal",
                                     color=color, color_42=color_42,
                                     gen_time=gen_time)
            maze_gen.create_output_file()
            solver = Dijkstras(config, maze_gen)
            path = solver.solve(is_new_maze=True)
            path = path[:-1]

        elif request == '4':
            if draw_path:
                draw_path = False
            else:
                draw_path = True

        elif request == '5':
            print("")
            print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            print("    █                          █")
            print("    █ 1: Change width  (min 9) █")
            print("    █                          █")
            print("    █ 2: Change height (min 7) █")
            print("    █                          █")
            print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█\n")

            request: str = input(f"{t.yellow} --->  {t.end}")
            while request != '1' and request != '2':
                if ' ' in request:
                    print("No space in request !")
                else:
                    print(f"{request} is INVALID ! Need 1 OR 2")
                request: str = input(f"{t.yellow} --->  {t.end}")

            if request == '1':
                print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
                print("    █                   █")
                print("    █ ENTER NEW WIDTH:  █")
                print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
                request: str = input(f"{t.yellow} --->  {t.end}")
                try:
                    request = int(request)
                    if request < 9:
                        raise ValueError
                    width_valid: bool = True
                except Exception:
                    print(f"The input: {request} is not a number or"
                          "not superieur to 8")
                    width_valid: bool = False

                while not width_valid:
                    try:
                        request: str = input(f"{t.yellow} --->  {t.end}")
                        request = int(request)
                        if request < 9:
                            raise ValueError
                        width_valid = True
                    except Exception:
                        print(f"The input: {request} is not a number or"
                              "not superieur to 8")

                width: int = int(request)
                height: None = None

            elif request == '2':
                print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
                print("    █                   █")
                print("    █ ENTER NEW HEIGHT: █")
                print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
                request: str = input(f"{t.yellow} --->  {t.end}")
                try:
                    request = int(request)
                    if request < 7:
                        raise ValueError
                    width_valid: bool = True
                except Exception:
                    print(f"The input: {request} is not a number or"
                          "not superieur to 6")
                    width_valid: bool = False

                while not width_valid:
                    try:
                        request: str = input(f"{t.yellow} --->  {t.end}")
                        request = int(request)
                        if request < 9:
                            raise ValueError
                        width_valid = True
                    except Exception:
                        print(f"The input: {request} is not a number or"
                              "not superieur to 8")

                height: int = int(request)
                width: None = None
            if height:
                config.height = height
                config.exit_y = height - 1
            if width:
                config.width = width
                config.exit_x = width - 1
            config.entry_x = 0
            config.entry_y = 0
            maze_gen = MazeGenerator(config=config,
                                     algorithm="kruskal", color=color,
                                     color_42=color_42, gen_time=gen_time)
            maze_gen.create_output_file()
            solver = Dijkstras(config, maze_gen)
            path = solver.solve(is_new_maze=True)
            path = path[:-1]

        elif request == '6':
            pass

        elif request == '7':
            pass

        elif request == '8':
            print("    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            print("    █                                  █")
            print("    █ ENTER NEW Time (ex = 0.05):      █")
            print("    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
            request: str = input(f"{t.yellow} --->  {t.end}")
            try:
                request = request
                width_valid: bool = True
            except Exception:
                print(f"The input: {request} is not a number")
                width_valid: bool = False

            while not width_valid:
                try:
                    request: str = input(f"{t.yellow} --->  {t.end}")
                    request = request
                    width_valid = True
                except Exception:
                    print(f"The input: {request} is not a number")
            gen_time = float(request)
