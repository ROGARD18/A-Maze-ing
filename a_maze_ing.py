from utils.check_dep import check_dep
from utils.parsing import parsing
from utils.models import Config, Maze
from pydantic import ValidationError

# def get_instructions() -> str;
    

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
        print(f"Conf = {config}")
    except (ValidationError, KeyError) as e:
        print(f"{type(e).__name__}: {e}")
        return
    try:
        print("Initialazing the maze")
        maze = Maze(
            width=config.width,
            height=config.height,
            entry_x=config.entry_x,
            entry_y=config.entry_y,
            exit_x=config.exit_x,
            exit_y=config.exit_y,
            output_file=config.output_file,
            algorithm=config.algorithm
        )
        print(maze)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
