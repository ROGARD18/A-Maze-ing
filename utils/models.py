from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self
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
    output_file: str = Field(min_length=5, max_length=20)
    perfect: bool = Field(default=False)
    algorithm: str = Field()

    @model_validator(mode="after")
    def check_points(self) -> Self:
        if not self.output_file.endswith(".txt"):
            raise ValidationError("The output file have to be a .txt file.")

        if self.entry_x == self.exit_x and self.entry_y == self.exit_y:
            raise ValidationError("Error: Entry et Exit are the same points.")

        if self.entry_x > self.width or self.entry_y > self.height:
            raise ValidationError(
                "Error: Entry point is outside the area of the maze."
            )

        if self.exit_x > self.width or self.exit_y > self.height:
            raise ValidationError("Error: Exit point is outside the area of"
                                  "the maze.")

        return self

    @model_validator(mode="after")
    def is_valid_algorithm(self) -> Self:
        valid_algo: list[str] = ["kruskal", "prism", "wilson"]
        if not (self.algorithm in valid_algo):
            raise ValidationError("Please chose one of the following"
                                  f"algorithm {valid_algo} or delete the key")
        return self


class Cell(BaseModel):
    west: int
    south: int
    east: int
    north: int
    set_id: int = Field(ge=0)
    in_path: bool = Field(default=False)


# types
Maze = list[list[Cell]]


class Algorithm(ABC):

    @abstractmethod
    def generate(self) -> Maze:
        pass

    def make_42(self, config: Config, maze: Maze) -> list[Cell]:
        width = config.width
        height = config.height
        list_42s: list[Cell] = []

        # The 4 of 42
        list_42s.append(maze[height // 2][width // 2 - 1])
        list_42s.append(maze[height // 2][width // 2 - 2])
        list_42s.append(maze[height // 2][width // 2 - 3])
        list_42s.append(maze[height // 2 - 1][width // 2 - 3])
        list_42s.append(maze[height // 2 - 2][width // 2 - 3])

        list_42s.append(maze[height // 2 + 1][width // 2 - 1])
        list_42s.append(maze[height // 2 + 2][width // 2 - 1])

        list_42s.append(maze[height // 2][width // 2 + 1])
        list_42s.append(maze[height // 2][width // 2 + 2])
        list_42s.append(maze[height // 2][width // 2 + 3])

        list_42s.append(maze[height // 2 + 1][width // 2 + 1])
        list_42s.append(maze[height // 2 + 2][width // 2 + 1])

        list_42s.append(maze[height // 2 + 2][width // 2 + 1])
        list_42s.append(maze[height // 2 + 2][width // 2 + 2])
        list_42s.append(maze[height // 2 + 2][width // 2 + 3])

        list_42s.append(maze[height // 2 - 1][width // 2 + 3])
        list_42s.append(maze[height // 2 - 2][width // 2 + 3])

        list_42s.append(maze[height // 2 - 2][width // 2 + 1])
        list_42s.append(maze[height // 2 - 2][width // 2 + 2])

        return list_42s
