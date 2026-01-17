# afomin

from enum import Enum


class CellType(Enum):
    NOTYPE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    ISOLATED = 3
    ENTRY = 4
    EXIT = 5
    PATH = 6


class Cell:
    def __init__(
            self,
            bottom_wall: bool = True,
            right_wall: bool = True
    ) -> None:
        self.bottom_wall = bottom_wall
        self.right_wall = right_wall
        self.__type: CellType = CellType.NOTYPE

    def set_type(self, new_type: CellType) -> None:
        if isinstance(new_type, CellType):
            self.__type = new_type
        else:
            raise Exception("[ERROR] Invalid type")

    def get_type(self) -> CellType:
        return self.__type


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry_pt: tuple[int, int],
        exit_pt: tuple[int, int]
    ) -> None:
        if height <= 0 or width <= 0:
            raise Exception("[ERROR] Maze width and height should be > 0.")
        self.__height: int = height
        self.__width: int = width
        self.__grid: list[list[Cell]] = [
                [Cell() for _ in range(width)]
                for _ in range(height)
                ]
        self.__entry: tuple[int, int] = entry_pt
        self.__exit: tuple[int, int] = exit_pt

        x, y = entry_pt
        self.__grid[y][x].set_type(CellType.ENTRY)
        x, y = exit_pt
        self.__grid[y][x].set_type(CellType.EXIT)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.__grid[y][x]

    def get_hex_of_cell(self, x: int, y: int) -> str:
        hex_output: int = 0b0000
        grid = self.get_grid()
        hex_chars: dict[int, str] = {
            0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
            5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'
        }
        if grid[y][x].get_type() == CellType.ISOLATED:
            return hex_chars[0b1111]
        if y == 0:
            hex_output |= 0b0001
        else:
            if grid[y - 1][x].bottom_wall is True:
                hex_output |= 0b0001
        if grid[y][x].right_wall is True:
            hex_output |= 0b0010
        if grid[y][x].bottom_wall is True:
            hex_output |= 0b0100
        if x == 0:
            hex_output |= 0b1000
        else:
            if grid[y][x - 1].right_wall is True:
                hex_output |= 0b1000
        return hex_chars[hex_output]

    def get_grid(self) -> list[list[Cell]]:
        return self.__grid

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_entry(self) -> tuple[int, int]:
        return self.__entry

    def get_exit(self) -> tuple[int, int]:
        return self.__exit
