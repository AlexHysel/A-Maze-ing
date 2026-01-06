from enum import Enum


class Type(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    NO_AXIS = 2
    START = 3
    FINISH = 4


class Cell:
    def __init__(self, bottom_wall=True, right_wall=True):
        self.bottom_wall = bottom_wall
        self.right_wall = right_wall
        self.__axis = None

    def set_type(self, axis):
        if axis >= 0 and axis <= 4:
            self.__axis = Type(axis)
        else:
            raise Exception("[ERROR] Invalid axis")

    def get_axis(self):
        return self.__axis


class Maze:
    def __init__(self, width, height):
        if height <= 0 or width <= 0:
            raise Exception("[ERROR] Maze width and height should be > 0.")
        self.__height = height
        self.__width = width
        self.__grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def get(self, x, y):
        return self.__grid[y][x]

    def get_grid(self):
        return self.__grid

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height
