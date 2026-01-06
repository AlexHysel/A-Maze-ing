#afomin

from .models import Maze, Type


class MazeRenderer:
    @staticmethod
    def display(maze, show_axis=False):
        grid = maze.get_grid()
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        print("+" + "---+" * width)

        for y in range(height):
            row_str = "|"  # Left boundary
            for x in range(width):
                cell = grid[y][x]

                if show_axis and cell.get_axis() is not None:
                    ax = cell.get_axis()
                    if ax == Type.HORIZONTAL:
                        symbol = "-"
                    elif ax == Type.VERTICAL:
                        symbol = "|"
                    elif ax == Type.NO_AXIS:
                        symbol = "@"
                    elif ax == Type.START:
                        symbol = "S"
                    elif ax == Type.FINISH:
                        symbol = "F"
                    row_str += f" {symbol} "
                else:
                    row_str += "   "

                row_str += "|" if cell.right_wall else " "
            print(row_str)

            bottom_str = "+"  # Left corner
            for x in range(width):
                cell = grid[y][x]
                bottom_str += "---" if cell.bottom_wall else "   "
                bottom_str += "+"
            print(bottom_str)
