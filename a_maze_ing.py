from random import seed, random
from pydantic import ValidationError
from mazegen.models import Config
from utils.check_dep import check_dep
from utils.parsing import parsing
from Menu.menu import menu_loop


def main() -> None:
    config: Config | None = None
    try:
        print("Checking if all dependencies are installed...")
        check_dep()
        print("Deps well installed.\n")
    except Exception as e:
        print(e)
        return
    try:
        print("Parsing config file...")
        config = parsing()
        if not config:
            raise ValueError("Error: try with config.txt to refere some"
                             " parameters for the maze.")
        print("Config acquired")
    except (ValidationError, KeyError, ValueError) as e:
        if isinstance(e, ValueError) and not isinstance(e, ValidationError):
            print("Seed should be an integer or a float number")
            return
        print(f"{type(e).__name__}: {e}")
        return
    if config.seed:
        seed(float(config.seed))
    else:
        seed(random())
    menu_loop(config)


if __name__ == "__main__":
    main()
