from .parsing import parsing
from .check_dep import check_dep

def main() -> None:
    parsing()
    check_dep()


if __name__ == "__main__":
    main()
