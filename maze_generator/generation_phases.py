# afomin

from abc import ABC, abstractmethod
from .models import CellType, Maze, Cell
import random


# === Basic phase ===

class GenerationPhase(ABC):
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _RESET = '\033[0m'

    def __init__(self) -> None:
        self._start_message: str = f'{self.__class__.__name__} started.'
        self._finish_message: str = f'{self.__class__.__name__} finished.'

    @abstractmethod
    def apply(self, maze: Maze):
        pass

    def get_start_message(self):
        return self._start_message

    def get_finish_message(self):
        return self._finish_message


# === Phases ===

# Adds 42 Header at the middle if maze size is valid
# and start/finish collide with header
class Add42HeaderPhase(GenerationPhase):
    def __init__(self) -> None:
        self._start_message: str = 'Adding 42 Header...'
        self._finish_message: str = (
                f'{self._GREEN}42 Header added.{self._RESET}')

    def apply(self, maze: Maze) -> Maze:
        h: int = maze.get_height()
        w: int = maze.get_width()

        if h >= 5 and w >= 7:
            x: int = int(w / 2 - 3.5)
            y: int = int(h / 2 - 2.5)

            # alex did this
            header_positions = [
                    (x, y), (x, y + 1), (x, y + 2), (x + 1, y + 2),
                    (x + 2, y + 2), (x + 2, y + 3), (x + 2, y + 4),
                    (x + 4, y), (x + 5, y), (x + 6, y), (x + 6, y + 1),
                    (x + 4, y + 2), (x + 5, y + 2), (x + 6, y + 2),
                    (x + 4, y + 3), (x + 4, y + 4), (x + 5, y + 4),
                    (x + 6, y + 4)
            ]
            # Validation
            for pos in header_positions:
                if maze.get_cell(*pos).get_type() is not CellType.NOTYPE:
                    self._finish_message = (
                            f'{self._YELLOW}Cancelled,' +
                            f'{pos} already has type.{self._RESET}'
                            )
                    return maze
            # Assignment
            for pos in header_positions:
                maze.get_cell(*pos).set_type(CellType.ISOLATED)
        else:
            self._finish_message = (
                    f'{self._YELLOW}Cancelled, ' +
                    f'maze less than 5x7.{self._RESET}'
                    )
            raise Exception("Maze must be bigger than 5x7")
        return maze


# Assignes random axis to None-type cells.
class TypeAssignmentPhase(GenerationPhase):
    def __init__(
        self,
        seed: int | None = None
    ) -> None:
        self._start_message = 'Axis assignment...'
        self._finish_message = (
                f'{self._GREEN}' +
                f'Finished successfully.{self._RESET}'
                )
        self._seed = seed

    def apply(self, maze: Maze):
        if self._seed is not None:
            random.seed(self._seed)
        for row in maze.get_grid():
            for cell in row:
                if cell.get_type() is CellType.NOTYPE:
                    cell.set_type(CellType(random.randint(1, 2)))
        return maze


# andmarti
class AxisPostProcess(GenerationPhase):
    def __init__(self) -> None:
        self._start_message: str = 'Axis post process...'
        self._finish_message = (
                f'{self._GREEN}' +
                f'Finished successfully.{self._RESET}'
                )

    def apply(self, maze: Maze) -> Maze:
        counter: int = 0
        grid: list[list[Cell]] = maze.get_grid()
        height: int = len(grid)
        width: int = len(grid[0]) if height > 0 else 0
        for y in range(height - 1):
            counter = 0
            for x in range(width):
                if (
                    grid[y][x].get_type() == CellType.HORIZONTAL
                    and grid[y + 1][x].get_type() == CellType.VERTICAL
                ):
                    counter += 1
                else:
                    counter = 0
                if counter >= 3 and counter % 2 == 1:
                    grid[y][x - 1].set_type(CellType.VERTICAL)
                    grid[y + 1][x - 1].set_type(CellType.HORIZONTAL)
        for x in range(width - 1):
            counter = 0
            for y in range(height):
                if (
                    grid[y][x].get_type() == CellType.VERTICAL
                    and grid[y][x + 1].get_type() == CellType.HORIZONTAL
                ):
                    counter += 1
                else:
                    counter = 0
                if counter >= 3 and counter % 2 == 1:
                    grid[y - 1][x].set_type(CellType.HORIZONTAL)
                    grid[y - 1][x + 1].set_type(CellType.VERTICAL)
        for y in range(height):
            counter = 0
            for x in range(width):
                if grid[y][x].get_type() == CellType.VERTICAL:
                    counter += 1
                else:
                    counter = 0
                if counter % 4 == 0 and counter > 0:
                    grid[y][x - 1].set_type(CellType.HORIZONTAL)
        for x in range(width):
            counter = 0
            for y in range(height):
                if grid[y][x].get_type() == CellType.HORIZONTAL:
                    counter += 1
                else:
                    counter = 0
                if counter % 3 == 0 and counter > 0:
                    grid[y][x].set_type(CellType.VERTICAL)
        return maze


# Breaks the walls to make paths using carver,
# that goes through grid where it is possible
# and breaks the walls.
class PathBuildingPhase(GenerationPhase):
    def __init__(self, is_perfect: bool = True):
        self._start_message: str = 'Carving path...'
        self._finish_message: str = (
                f'{self._GREEN}All paths carved.{self._RESET}'
                )
        self._is_perfect: bool = is_perfect

    # Returns accessable cell where carver can go
    def _next_pos(
            self,
            maze: Maze,
            neighbours: dict[str, tuple[int, int]],
            visited: set[tuple[int, int]]
            ) -> tuple[int, int] | None:
        directions: list[str] = list(neighbours)
        random.shuffle(directions)

        for direction in directions:
            pos: tuple[int, int] = neighbours[direction]
            if pos not in visited:
                c_type: CellType = maze.get_cell(*pos).get_type()
                if direction in ['right', 'left']:
                    if (
                        c_type == CellType.HORIZONTAL
                        or c_type == CellType.EXIT
                    ):
                        return pos
                elif direction in ['bottom', 'top']:
                    if (
                        c_type == CellType.VERTICAL
                        or c_type == CellType.EXIT
                    ):
                        return pos

            # If its not perfect there is 3% chance to break the wall anyway
            elif (
                not self._is_perfect
                and random.random() < 0.03
                and maze.get_cell(*pos).get_type() is not CellType.ISOLATED
            ):
                return pos
        return None

    # Breaks wall between next_pos and carver_cell
    def _break_wall(
            self,
            maze: Maze,
            n_x: int,
            n_y: int,
            x: int,
            y: int
    ) -> None:
        if n_y - y == 1:
            maze.get_cell(x, y).bottom_wall = False
        if n_x - x == 1:
            maze.get_cell(x, y).right_wall = False
        if n_y - y == -1:
            maze.get_cell(x, y - 1).bottom_wall = False
        if n_x - x == -1:
            maze.get_cell(x - 1, y).right_wall = False

    # Returns neighbour cells ignoring their type
    def _neighbour_cells(
            self,
            maze: Maze,
            x: int,
            y: int
            ) -> dict[str, tuple[int, int]]:
        neighbours: dict[str, tuple[int, int]] = {}
        if y + 1 < maze.get_height():
            neighbours['bottom'] = (x, y + 1)
        if x + 1 < maze.get_width():
            neighbours['right'] = (x + 1, y)
        if y > 0:
            neighbours['top'] = (x, y - 1)
        if x > 0:
            neighbours['left'] = (x - 1, y)
        return neighbours

    # Happens if we have isolated parts.
    # Finds visited cell with not visited neighbour,
    # breaks the wall between them and returns
    # new cell to start new route
    def _break_frontier(
            self,
            maze: Maze,
            visited: set[tuple[int, int]]
    ) -> tuple[int, int]:
        inner_pos: tuple[int, int] = (0, 0)
        outer_pos: tuple[int, int] = (0, 0)
        for inner_pos in visited:
            if maze.get_cell(*inner_pos).get_type() == CellType.ISOLATED:
                continue
            neighbours: dict[str, tuple[int, int]] = (
                    self._neighbour_cells(maze, *inner_pos)
                    )
            for direction, outer_pos in neighbours.items():
                if outer_pos not in visited:
                    visited.add(outer_pos)
                    self._break_wall(maze, *outer_pos, *inner_pos)
                    return outer_pos
        return outer_pos

    # Adds header to visited to prevent any
    # actions on it
    def _fill_with_unreachable(
            self,
            maze: Maze,
            visited: set[tuple[int, int]]
            ) -> None:
        for y in range(maze.get_height()):
            for x in range(maze.get_width()):
                if maze.get_cell(x, y).get_type() == CellType.ISOLATED:
                    visited.add((x, y))

    def apply(self, maze: Maze) -> Maze:
        route: list[tuple[int, int]] = [maze.get_entry()]
        visited: set[tuple[int, int]] = set()
        cell_count: int = maze.get_width() * maze.get_height()

        self._fill_with_unreachable(maze, visited)

        while len(visited) < cell_count:
            if not route:
                route.append(self._break_frontier(maze, visited))
            carver_pos = route[-1]

            visited.add(carver_pos)
            neighbours: dict[str, tuple[int, int]] = (
                    self._neighbour_cells(maze, *carver_pos)
                    )
            next_pos = self._next_pos(maze, neighbours, visited)

            if next_pos is None:
                route.pop()
            else:
                self._break_wall(maze, *next_pos, *carver_pos)
                route.append(next_pos)
        return maze
