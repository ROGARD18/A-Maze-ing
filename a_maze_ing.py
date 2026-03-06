from utils.check_dep import check_dep
from utils.parsing import parsing
from utils.models import Config, Maze

# def get_instructions() -> str;
    

def main() -> None:
    config: Config | None = None
    try:
        print("Checking if all dependencies are installed...")
        check_dep()
        print("Deps well installed.\n")
        print("Parsing config file...")
        config = parsing()
        print("Config acquired")
        print("Initialazing the maze")
        maze = Maze(
            width=config.width,
            height=config.height,
            entry_x=config.entry_x,
            entry_y=config.entry_y,
            exit_x=config.exit_x,
            exit_y=config.exit_y,
            output_file=config.output_file
        )
        print(maze)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
