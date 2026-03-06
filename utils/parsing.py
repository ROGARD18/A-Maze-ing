import sys
from utils.models import NoArgumentError, Config
from typing import Any


def parsing() -> Config:

    config_dict: dict[str, Any] = {}
    is_algo_present: bool = False

    if (len(sys.argv) < 2):
        raise NoArgumentError("Error: try with config.txt to refere some"
                              " parameters for the maze.")
    with open(sys.argv[1], 'r') as file:
        file_content = file.read()

    for line in file_content.split('\n'):
        if 'ENTRY' in line:
            x, y = (line.split('='))[1].split(',')
            config_dict.update({'ENTRY_X': x})
            config_dict.update({'ENTRY_Y': y})

        elif 'EXIT' in line:
            x, y = (line.split('='))[1].split(',')
            config_dict.update({'EXIT_X': x})
            config_dict.update({'EXIT_Y': y})
        else:
            key, value = line.split('=')
            if (key == 'ALGORITHM'):
                is_algo_present = True
            config_dict.update({key: value})

    if is_algo_present:
        algo = config_dict['ALGORITHM']
    else:
        algo = "kruskal"
    config_obj: Config = Config(
        width=config_dict['WIDTH'],
        height=config_dict['HEIGHT'],
        entry_x=config_dict['ENTRY_X'],
        entry_y=config_dict['ENTRY_Y'],
        exit_x=config_dict['EXIT_X'],
        exit_y=config_dict['EXIT_Y'],
        output_file=config_dict['OUTPUT_FILE'],
        perfect=config_dict['PERFECT'],
        algorithm=algo
    )

    return config_obj
