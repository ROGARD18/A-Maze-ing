from utils import check_dep


def main() -> None:
    try:
        check_dep()
        print("--------------------------------------------------check_dep no crash")
        from utils import parsing
        parsing()
        print("--------------------------------------------------parsing no crash")
    except Exception as e:
        print(e)
        print("Steps:\n-make install\n-make run")
    print ("No crash")

import pydantic

if __name__ == "__main__":
    main()
