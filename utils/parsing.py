from pydantic import BaseModel, Field, ValidationError, model_validator
from typing_extensions import Self
import sys


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

    @model_validator(mode='after')
    def check_points(self) -> Self:
        if not self.output_file.endswith('.txt'):
            raise ValueError("The output file have to be a .txt file.")
        
        if self.entry_x == self.exit_x and self.entry_y == self.exit_y:
            raise ValueError("Error: Entry et Exit are the same points.")
        
        if self.entry_x > self.width or self.entry_y > self.height:
            raise ValueError(f"Error: Entry point is outside the area of the maze.")
        
        if self.exit_x > self.width or self.exit_y > self.height:
            raise ValueError(f"Error: Exit point is outside the area of the maze.")
        
        return self


def parsing() -> None:

    config_dict = {}

    if (len(sys.argv) < 2):
        raise NoArgumentError("Error: try with config.txt to refere some"
                              " parameters for the maze.")
    try:
        with open(sys.argv[1], 'r') as file:
            file_content = file.read()
    except Exception as e:
        raise (e)

    for line in file_content.split('\n'):
        if 'ENTRY' in line:
            x, y = (line.split('='))[1].split(',')
            config_dict.update({'ENTRY_X': x})
            config_dict.update({'ENTRY_Y': y})

        elif 'EXIT' in line:
            x, y = (line.split('='))[1].split(',')
            config_dict.update({'EXIT_X': x})
            config_dict.update({'EXIT_Y': y})
        else:
            key, value = line.split('=')
            config_dict.update({key: value})
    try:
        config_obj = Config(
            width=config_dict['WIDTH'],
            height=config_dict['HEIGHT'],
            entry_x=config_dict['ENTRY_X'],
            entry_y=config_dict['ENTRY_Y'],
            exit_x=config_dict['EXIT_X'],
            exit_y=config_dict['EXIT_Y'],
            output_file=config_dict['OUTPUT_FILE'],
            perfect=config_dict['PERFECT']
        )
        print(config_obj.width)
    except ValidationError as e:
        print(e.errors()[0]['msg'])
        raise Exception
    print(config_dict)
