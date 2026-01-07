#afomin

from enum import Enum
from typing import Tuple


class Type(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    ISOLATED = 2
    ENTRY = 3
    EXIT = 4


class Cell:
    def __init__(self, bottom_wall=True, right_wall=True):
        self.bottom_wall = bottom_wall
        self.right_wall = right_wall
        self.__type = None

    def set_type(self, new_type: Type):
        if isinstance(new_type, Type):
            self.__type = new_type
        else:
            raise Exception("[ERROR] Invalid type")

    def get_type(self):
        return self.__type


class Maze:
    def __init__(self, width: int, height: int, entry_pt: Tuple[int, int], exit_pt: Tuple[int, int]):
        if height <= 0 or width <= 0:
            raise Exception("[ERROR] Maze width and height should be > 0.")
        self.__height = height
        self.__width = width
        self.__grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.__entry = entry_pt
        self.__exit = exit_pt

        x, y = entry_pt
        self.__grid[y][x].set_type(Type.ENTRY)
        x, y = exit_pt
        self.__grid[y][x].set_type(Type.EXIT)

    def get(self, x, y):
        return self.__grid[y][x]

    def get_grid(self):
        return self.__grid

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_entry(self):
        return self.__entry

    def get_exit(self):
        return self.__exit
