from MazeGen.generator import MazeGenerator
from utils.models import Config
from random import choice
import os


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
    faint = "\u001b[2m"


def menu_loop(config: Config) -> None:
    flag_first: bool = True

    t = Colors
    colors_list: list[str] = [t.yellow, t.red, t.green, t.blue, t.cyan,
                              t.magenta, t.white]

    color: str = choice(colors_list)
    color_42: str = choice(colors_list)

    while True:
        os.system('clear')

        if flag_first:
            maze_gen = MazeGenerator(config=config, algorithm="kruskal")
            maze_gen.create_output_file()
            flag_first = False
        maze_gen.draw_maze(color, color_42)

        print("\n\n  __        _  _   __   ____  ____      __  __ _   "
              "___ \n"
              " / _\\  ___ ( \\/ ) / _\\ (__  )(  __) ___ (  )(  ( \\ / __)\n"
              "/    \\(___)/ \\/ \\/    \\ / _/  ) _) (___) )( /    /( (_ \\\n"
              "\\_/\\_/     \\_)(_/\\_/\\_/(____)(____)     (__)\\_)__) \\___/")

        print("\n         --- MENU ---")
        print(" ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
        print(" █                           █")
        print(" █ 1: Change walls color     █")
        print(" █                           █")
        print(" █ 2: Change 42 color        █")
        print(" █                           █")
        print(" █ 3: Generate new maze      █")
        print(" █                           █")
        print(" █ 4: Show path (shortest)   █")
        print(" █                           █")
        print(" █ q: Exit                   █")
        print(" █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print("")

        request: str = input('->  ')
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
            pass
