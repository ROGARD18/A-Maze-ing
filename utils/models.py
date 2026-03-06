from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self


class NoArgumentError(Exception):
    pass


class Config(BaseModel):
    width: int = Field(ge=0, le=1000)
    height: int = Field(ge=0, le=1000)
    entry_x: int = Field(ge=0, le=1000)
    entry_y: int = Field(ge=0, le=1000)
    exit_x: int = Field(ge=0, le=1000)
    exit_y: int = Field(ge=0, le=1000)
    output_file: str = Field(min_length=5, max_length=20)
    perfect: bool = Field(default=False)
    algorithm: str | None = Field(default="kruskal")

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
        valid_algo: list[str] = ["kruskal", "Prism", "Wilson"]
        if not self.algorithm in valid_algo:
            raise ValidationError(f"Please chose one of the following algorithm "
                                  f"{valid_algo} or let it empty")
        return self

class Cell(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    walls: str = Field(min_length=4, max_length=4)


class Maze(Config, BaseModel):
    entry: Cell | None = Field(default=None)
    exit: Cell | None = Field(default=None)
    cells: list[Cell] | None = Field(default=None)
