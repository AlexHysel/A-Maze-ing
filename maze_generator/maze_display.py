#afomin

from .models import Maze, Type


class MazeRenderer:
    @staticmethod
    def display(maze, show_axis=False):
        BLUE = '\033[94m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        RESET = '\033[0m'

        grid = maze.get_grid()
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        print("+" + "---+" * width)

        for y in range(height):
            row_str = "|" 
            
            for x in range(width):
                cell = grid[y][x]
                
                cell_type = cell.get_type()
                mapping = {
                    Type.ISOLATED: f"{BLUE}@{RESET}",
                    Type.ENTRY: f"{RED}S{RESET}",
                    Type.EXIT: f"{GREEN}X{RESET}"
                }
                if show_axis:
                    mapping[Type.HORIZONTAL] = '-'
                    mapping[Type.VERTICAL] = '|'

                symbol = mapping.get(cell_type, " ")
                row_str += f" {symbol} "
                
                row_str += "|" if cell.right_wall else " "
            
            print(row_str)

            bottom_str = "+"
            for x in range(width):
                cell = grid[y][x]
                bottom_str += "---" if cell.bottom_wall else "   "
                bottom_str += "+"
            print(bottom_str) 
