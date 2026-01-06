#afomin

from .models import Maze, Type


class MazeRenderer:
    @staticmethod
    def display(maze, show_type=False):
        grid = maze.get_grid()
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        # 1. Top Outer Border
        # Since cells don't have a 'top_wall', we draw a solid line for the roof
        print("+" + "---+" * width)

        for y in range(height):
            # 2. Left Outer Border 
            # We start every row with a '|' to form the left exterior wall
            row_str = "|" 
            
            for x in range(width):
                cell = grid[y][x]
                
                # Determine symbol to display
                symbol = " "
                if show_type:
                    ax = cell.get_type()
                    mapping = {
                        Type.HORIZONTAL: "-",
                        Type.VERTICAL: "|",
                        Type.NO_AXIS: "@",
                        Type.START: "S",
                        Type.FINISH: "F"
                    }
                    symbol = mapping.get(ax, " ")
                
                row_str += f" {symbol} "
                
                # 3. Right Walls (Internal or Right Exterior)
                row_str += "|" if cell.right_wall else " "
            
            print(row_str)

            # 4. Bottom Walls (Internal or Bottom Exterior)
            bottom_str = "+"
            for x in range(width):
                cell = grid[y][x]
                bottom_str += "---" if cell.bottom_wall else "   "
                bottom_str += "+"
            print(bottom_str) 
