from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self
import sys


class PointError(ValidationError):
    pass


class NoArgumentError(Exception):
    pass


class Config(BaseModel):
    width: int = Field(ge=9)
    height: int = Field(ge=3)
    entry_x: tuple = Field()
    entry_y: int = Field()
    exit_x: tuple = Field()
    exit_y: int = Field()
    output_file: str = Field()
    perfect: bool = False

    @model_validator(mode='after')
    def check_points(self) -> Self:
        if self.entry_x == self.exit_x and self.entry_y == self.exit_y:
            raise PointError("Error: Entry et Exit are the same points.")
        return self


def parsing() -> None:

    config_dict = {}

    if (len(sys.argv) < 2):
        raise NoArgumentError("Error: try with config.txt to refere some"
                              " parameters for the maze.")
    with open(sys.argv[1], 'r') as file:
        file_content = file.read()
    for line, in file_content.split('\n'):
        key, value = line.split(':')
        config_dict.update({key: value})
    print(config_dict)
