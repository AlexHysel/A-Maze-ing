# afomin

from .models import Maze, CellType, Cell


class MazeRenderer:
    @staticmethod
    def display(maze: Maze, show_axis=False):
        BLUE: str = '\033[94m'
        RED: str = '\033[41m'
        GREEN: str = '\033[42m'
        RESET: str = '\033[0m'

        grid: list[list[Cell]] = maze.get_grid()
        height: int = len(grid)
        width: int = len(grid[0]) if height > 0 else 0

        print("+" + "---+" * width)

        for y in range(height):
            row_str: str = "|"

            for x in range(width):
                cell: Cell = grid[y][x]

                cell_type: CellType = cell.get_type()
                mapping: dict[CellType, str] = {
                    CellType.ISOLATED: f"{BLUE}@{RESET}",
                    CellType.ENTRY: f"{RED}S{RESET}",
                    CellType.EXIT: f"{GREEN}X{RESET}",
                    CellType.PATH: "."
                }
                if show_axis:
                    mapping[CellType.HORIZONTAL] = '-'
                    mapping[CellType.VERTICAL] = '|'

                symbol: str = mapping.get(cell_type, " ")
                row_str += f" {symbol} "

                row_str += "|" if cell.right_wall else " "

            print(row_str)

            bottom_str: str = "+"
            for x in range(width):
                cell = grid[y][x]
                bottom_str += "---" if cell.bottom_wall else "   "
                bottom_str += "+"
            print(bottom_str)

    @staticmethod
    def print_formatted_output(maze: Maze) -> None:
        grid: list[list[Cell]] = maze.get_grid()
        height: int = len(grid)
        width: int = len(grid[0]) if height > 0 else 0
        x: int
        y: int
        for y in range(height):
            for x in range(width):
                print(maze.get_hex_of_cell(x, y), end="")
            print()
        print()
        x, y = maze.get_entry()
        print(x, ", ", y, sep="")
        x, y = maze.get_exit()
        print(x, ", ", y, sep="")
