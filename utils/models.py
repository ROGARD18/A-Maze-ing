from pydantic import BaseModel, Field
from pydantic import model_validator, ConfigDict
from typing_extensions import Self, Optional
from abc import ABC, abstractmethod


class NoArgumentError(Exception):
    pass


class Config(BaseModel):
    width: int = Field(ge=9, le=1000)
    height: int = Field(ge=7, le=1000)
    entry_x: int = Field(ge=0, le=1000)
    entry_y: int = Field(ge=0, le=1000)
    exit_x: int = Field(ge=0, le=1000)
    exit_y: int = Field(ge=0, le=1000)
    output_file: str = Field(min_length=5, max_length=30)
    perfect: bool = Field()
    algorithm: str = Field()
    seed: float | None = Field(default=None)

    @model_validator(mode="after")
    def check_points(self) -> Self:
        if not self.output_file.endswith(".txt"):
            raise ValueError("The output file have to be a .txt file.")

        if self.entry_x == self.exit_x and self.entry_y == self.exit_y:
            raise ValueError("Entry and Exit cannot be the same point.")

        if self.entry_x > self.width - 1 or self.entry_y > self.height - 1:
            raise ValueError(
                f"Entry ({self.entry_x},{self.entry_y}) is outside the grid "
                f"({self.width}x{self.height})."
            )

        if self.exit_x > self.width - 1 or self.exit_y > self.height - 1:
            raise ValueError(
                f"Exit ({self.exit_x},{self.exit_y}) is outside the grid "
                f"({self.width}x{self.height})."
            )

        return self

    @model_validator(mode="after")
    def check_not_in_42(self) -> Self:
        cells_42_coords = self.get_42_coords()
        if (self.entry_x, self.entry_y) in cells_42_coords:
            raise ValueError(
                f"Entry ({self.entry_x},{self.entry_y}) is inside the 42 zone."
            )
        if (self.exit_x, self.exit_y) in cells_42_coords:
            raise ValueError(
                f"Exit ({self.exit_x},{self.exit_y}) is inside the 42 zone."
            )
        return self

    def get_42_coords(self) -> list[tuple[int, int]]:
        w = self.width
        h = self.height
        coords: list[tuple[int, int]] = []

        coords.append((w // 2 - 1, h // 2))
        coords.append((w // 2 - 2, h // 2))
        coords.append((w // 2 - 3, h // 2))
        coords.append((w // 2 - 3, h // 2 - 1))
        coords.append((w // 2 - 3, h // 2 - 2))

        coords.append((w // 2 - 1, h // 2 + 1))
        coords.append((w // 2 - 1, h // 2 + 2))

        coords.append((w // 2 + 1, h // 2))
        coords.append((w // 2 + 2, h // 2))
        coords.append((w // 2 + 3, h // 2))

        coords.append((w // 2 + 1, h // 2 + 1))
        coords.append((w // 2 + 1, h // 2 + 2))

        coords.append((w // 2 + 1, h // 2 + 2))
        coords.append((w // 2 + 2, h // 2 + 2))
        coords.append((w // 2 + 3, h // 2 + 2))

        coords.append((w // 2 + 3, h // 2 - 1))
        coords.append((w // 2 + 3, h // 2 - 2))

        coords.append((w // 2 + 1, h // 2 - 2))
        coords.append((w // 2 + 2, h // 2 - 2))

        return coords

    @model_validator(mode="after")
    def is_valid_algorithm(self) -> Self:
        valid_algo: list[str] = ["kruskal", "prism", "wilson"]
        if self.algorithm not in valid_algo:
            raise ValueError(
                f"Invalid algorithm '{self.algorithm}'. "
                f"Choose from {valid_algo} or remove the key."
            )
        return self


class Cell(BaseModel):
    model_config = ConfigDict(frozen=False)

    west: int
    south: int
    east: int
    north: int
    set_id: int
    y: int
    x: int
    is_entry: bool
    is_exit: bool
    in_path: Optional[bool] = Field(default=False)

    def __hash__(self) -> int:
        return hash((self.y, self.x))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return self.y == other.y and self.x == other.x


# types
Grid = list[list[Cell]]


class Maze(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate(self, animated: bool, color: str, color_42: str,
                 gen_time: float) -> Grid:
        pass

    def make_42(self, config: Config, grid: Grid) -> list[Cell]:
        width = config.width
        height = config.height
        list_42s: list[Cell] = []

        # The 4 of 42
        list_42s.append(grid[height // 2][width // 2 - 1])
        list_42s.append(grid[height // 2][width // 2 - 2])
        list_42s.append(grid[height // 2][width // 2 - 3])
        list_42s.append(grid[height // 2 - 1][width // 2 - 3])
        list_42s.append(grid[height // 2 - 2][width // 2 - 3])

        list_42s.append(grid[height // 2 + 1][width // 2 - 1])
        list_42s.append(grid[height // 2 + 2][width // 2 - 1])

        list_42s.append(grid[height // 2][width // 2 + 1])
        list_42s.append(grid[height // 2][width // 2 + 2])
        list_42s.append(grid[height // 2][width // 2 + 3])

        list_42s.append(grid[height // 2 + 1][width // 2 + 1])
        list_42s.append(grid[height // 2 + 2][width // 2 + 1])

        list_42s.append(grid[height // 2 + 2][width // 2 + 1])
        list_42s.append(grid[height // 2 + 2][width // 2 + 2])
        list_42s.append(grid[height // 2 + 2][width // 2 + 3])

        list_42s.append(grid[height // 2 - 1][width // 2 + 3])
        list_42s.append(grid[height // 2 - 2][width // 2 + 3])

        list_42s.append(grid[height // 2 - 2][width // 2 + 1])
        list_42s.append(grid[height // 2 - 2][width // 2 + 2])

        return list_42s
