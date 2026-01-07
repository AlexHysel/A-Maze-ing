#afomin

from .models import Maze, Type


class MazeRenderer:
    @staticmethod
    def display(maze, show_type=False):
        grid = maze.get_grid()
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        print("+" + "---+" * width)

        for y in range(height):
            row_str = "|" 
            
            for x in range(width):
                cell = grid[y][x]
                
                symbol = " "
                ax = cell.get_type()
                if show_type:
                    mapping = {
                        Type.HORIZONTAL: "-",
                        Type.VERTICAL: "|"
                    }
                    symbol = mapping.get(ax, " ")
                mapping = {
                    Type.NO_AXIS: "@",
                    Type.START: "S",
                    Type.FINISH: "F"
                }
                symbol = mapping.get(ax, " ")
                row_str += f" {symbol} "
                
                row_str += "|" if cell.right_wall else " "
            
            print(row_str)

            bottom_str = "+"
            for x in range(width):
                cell = grid[y][x]
                bottom_str += "---" if cell.bottom_wall else "   "
                bottom_str += "+"
            print(bottom_str) 
