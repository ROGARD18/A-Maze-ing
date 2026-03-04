from pydantic import Field, BaseModel, model_validator, ValidationError
from typing import Self

class Cell(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    

class Maze(BaseModel):
    width: int = Field(ge=9)
    heigh: int = Field(ge=8)
    entry: Cell
    exit: Cell
    cells: list[Cell] | None = Field(default=None)
    perfect: bool = Field(default=False)
    output_file: str

    @model_validator(mode="after")
    def valid_maze(self) -> Self:
        if self.entry == self.exit:
            raise ValidationError("Entry and exit must be different")
        return self


def main() -> None:
    pass


if __name__ == "__main__":
    main()
