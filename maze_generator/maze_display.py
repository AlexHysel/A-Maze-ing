# afomin

from .models import Maze, CellType, Cell
from MazeSolver.maze_solver import MazeSolver


class MazeRenderer:
    RESET: str = '\033[0m'
    COLORS: list[str] = ['\033[94m', '\033[92m', '\033[93m', '\033[91m']
    RED_BG: str = '\033[41m'
    GREEN_BG: str = '\033[42m'

    def __init__(self) -> None:
        self._clr_index = 0
        self._clr0 = MazeRenderer.COLORS[0]
        self._clr1 = MazeRenderer.COLORS[1]

    def rotate_color(self) -> None:
        self._clr0s_num = len(MazeRenderer.COLORS)
        index = (self._clr_index + 1) % self._clr0s_num
        self._clr_index = index
        self._clr0 = MazeRenderer.COLORS[index]
        self._clr1 = MazeRenderer.COLORS[(index + 1) % self._clr0s_num]

    def _assign_path(
            maze,
            path: str | None
            ) -> Maze:
        if path is None:
            return maze
        height: int = maze.get_height()
        width: int = maze.get_width()
        curr: tuple[int, int] = maze.get_entry()
        for move in path:
            if move == 'N':
                curr = (curr[0], curr[1] - 1)
            elif move == 'E':
                curr = (curr[0] + 1, curr[1])
            elif move == 'S':
                curr = (curr[0], curr[1] + 1)
            elif move == 'W':
                curr = (curr[0] - 1, curr[1])
            else:
                raise Exception('invalid character in path string')
            if curr[0] < 0 or curr[0] >= width:
                raise Exception('path went outside of bounds')
            if curr[1] < 0 or curr[1] >= height:
                raise Exception('path went outside of bounds')
            if (curr != maze.get_entry() and curr != maze.get_exit()):
                maze.get_cell(*curr).set_type(CellType.PATH)

    def display(
            self,
            maze: Maze,
            show_axis: bool = False,
            path: list[tuple[int, int]] | None = None,
            show_path: bool = False
            ) -> None:

        mapping: dict[CellType, str] = {
            CellType.HORIZONTAL: '-',
            CellType.VERTICAL: '|',
            CellType.ISOLATED: f'{self._clr1}@',
            CellType.ENTRY: f'{MazeRenderer.RED_BG}S{MazeRenderer.RESET}',
            CellType.EXIT: f'{MazeRenderer.GREEN_BG}X{MazeRenderer.RESET}',
        }

        h: int = maze.get_height()
        w: int = maze.get_width()

        print(f'{self._clr0}+' + '---+' * w)
        for y in range(h):

            # Cells
            row_str: str = f'{self._clr0}|{MazeRenderer.RESET}'
            for x in range(w):
                cell = maze.get_cell(x, y)
                cell_type = cell.get_type()

                if cell_type in [CellType.HORIZONTAL, CellType.VERTICAL]:
                    if show_path and (x, y) in path:
                        symbol = f'{MazeRenderer.RESET}.'
                    elif show_axis:
                        symbol: str = mapping.get(cell_type, ' ')
                    else:
                        symbol = ' '
                else:
                    symbol: str = mapping.get(cell_type, ' ')
                row_str += f' {symbol} '
                if cell.right_wall:
                    row_str += f'{self._clr0}' + f'|{MazeRenderer.RESET}'
                else:
                    row_str += ' '
            print(row_str)

            # Bottom walls
            print(f'{self._clr0}', end='')
            bottom_str: str = '+'
            for x in range(w):
                cell: Cell = maze.get_cell(x, y)
                bottom_str += '---' if cell.bottom_wall else '   '
                bottom_str += '+'
            print(bottom_str)

        print(f'{MazeRenderer.RESET}')

    @staticmethod
    def save_formatted_output(maze: Maze, path, filename: str) -> None:
        grid: list[list[Cell]] = maze.get_grid()
        height: int = len(grid)
        width: int = len(grid[0]) if height > 0 else 0
        x: int
        y: int
        out_str: str = ''
        for y in range(height):
            for x in range(width):
                out_str += maze.get_hex_of_cell(x, y)
            out_str += '\n'
        out_str += '\n'

        x, y = maze.get_entry()
        out_str += str(x)
        out_str += ', '
        out_str += str(y)
        out_str += '\n'

        x, y = maze.get_exit()
        out_str += str(x)
        out_str += ', '
        out_str += str(y)
        out_str += '\n'

        out_str += MazeSolver.get_path_str(path)
        out_str += '\n'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(out_str)
