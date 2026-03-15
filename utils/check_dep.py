class DependencyError(Exception):
    pass


def check_dep() -> None:
    try:
        import pydantic
    except Exception as e:
        raise DependencyError(f"Error miss dependency: {e}")
