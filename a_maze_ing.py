from parsing import parsing


def main() -> None:
    try:
        check_dep()
        parsing()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
