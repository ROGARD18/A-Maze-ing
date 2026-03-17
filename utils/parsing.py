import sys
from utils.models import NoArgumentError, Config
from typing import Any


def parsing() -> Config:

    config_dict: dict[str, Any] = {}
    is_algo_present: bool = False
    is_seed_present: bool = False

    if len(sys.argv) < 2:
        raise NoArgumentError("Error: try with config.txt to refere some"
                              " parameters for the maze.")
    with open(sys.argv[1], 'r') as file:
        file_content = file.read()

    for line in file_content.split('\n'):
        if not line.strip():
            continue
        if 'ENTRY' in line:
            parts = line.split('=')
            if len(parts) != 2 or ',' not in parts[1]:
                raise ValueError("ENTRY must be in format ENTRY=x,y")
            x, y = parts[1].split(',')
            if (not x.strip().lstrip('-').isdigit()
                    or not y.strip().lstrip('-').isdigit()):
                raise ValueError(
                    f"ENTRY coordinates must be integers, got: {parts[1]}")
            config_dict.update({'ENTRY_X': int(x.strip())})
            config_dict.update({'ENTRY_Y': int(y.strip())})
        elif 'EXIT' in line:
            parts = line.split('=')
            if len(parts) != 2 or ',' not in parts[1]:
                raise ValueError("EXIT must be in format EXIT=x,y")
            x, y = parts[1].split(',')
            if (not x.strip().lstrip('-').isdigit()
                    or not y.strip().lstrip('-').isdigit()):
                raise ValueError(
                    f"EXIT coordinates must be integers, got: {parts[1]}")
            config_dict.update({'EXIT_X': int(x.strip())})
            config_dict.update({'EXIT_Y': int(y.strip())})
        else:
            if '=' not in line:
                raise ValueError(f"Invalid config line: '{line}'")
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key == 'ALGORITHM':
                is_algo_present = True
            if key == 'SEED':
                is_seed_present = True
            config_dict.update({key: value})

    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY_X', 'ENTRY_Y',
                     'EXIT_X', 'EXIT_Y', 'OUTPUT_FILE', 'PERFECT']
    for k in required_keys:
        if k not in config_dict:
            raise KeyError(f"Missing required config key: '{k}'")

    algo = config_dict['ALGORITHM'] if is_algo_present else "kruskal"
    seed = float(config_dict['SEED']) if is_seed_present else None

    config_obj: Config = Config(
        width=int(config_dict['WIDTH']),
        height=int(config_dict['HEIGHT']),
        entry_x=config_dict['ENTRY_X'],
        entry_y=config_dict['ENTRY_Y'],
        exit_x=config_dict['EXIT_X'],
        exit_y=config_dict['EXIT_Y'],
        output_file=config_dict['OUTPUT_FILE'],
        perfect=config_dict['PERFECT'],
        algorithm=algo,
        seed=seed
    )

    return config_obj
