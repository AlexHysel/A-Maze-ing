#afomin

from abc import ABC, abstractmethod
from .models import Type
import random


# === Basic phase ===

class GenerationPhase(ABC):
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _RESET = '\033[0m'

    def __init__(self):
        self._start_message = f'{self.__class__.__name__} started.'
        self._finish_message = f'{self.__class__.__name__} finished.'

    @abstractmethod
    def apply(self, maze):
        pass

    def get_start_message(self):
        return self._start_message

    def get_finish_message(self):
        return self._finish_message


# === Phases ===

# Adds 42 Header at the middle if maze size is valid
# and start/finish collide with header

class Add42HeaderPhase(GenerationPhase):
    def __init__(self):
        self._start_message = 'Adding 42 Header...'
        self._finish_message = f'{self._GREEN}42 Header added.{self._RESET}'

    def apply(self, maze):
        h = maze.get_height()
        w = maze.get_width()

        if h >= 5 and w >= 7:
            x = int(w / 2 - 3.5)
            y = int(h / 2 - 2.5)

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
                if maze.get(*pos).get_type() is not None:
                    self._finish_message = f'{self._YELLOW}Cancelled, {pos} already has type.{self._RESET}'
                    return maze

            # Assignment
            for pos in header_positions:
                maze.get(*pos).set_type(Type.ISOLATED)

        else:
            self._finish_message = f'{self._YELLOW}Cancelled, maze less than 5x7.{self._RESET}'
        return maze


# Assignes random axis to None-type cells.

class TypeAssignmentPhase(GenerationPhase):
    def __init__(self, seed = None):
        self._start_message = f'Axis assignment...'
        self._finish_message = f'{self._GREEN}Finished successfully.{self._RESET}'
        if seed is not None:
            random.seed(seed)

    def apply(self, maze):
        for row in maze.get_grid():
            for cell in row:
                if cell.get_type() is None:
                    cell.set_type(Type(random.randint(0, 1)))
        return maze


# Breaks the walls to make paths using carver,
# that goes through grid where it is possible
# and breaks the walls.

class PathBuildingPhase(GenerationPhase):
    def __init__(self, is_perfect = True):
        self._start_message = 'Carving path...'
        self._finish_message = f'{self._GREEN}All paths carved.{self._RESET}'
        self._is_perfect = is_perfect

    # Returns accessable cell where carver can go
    def _next_pos(self, maze, neighbours, visited):
        grid = maze.get_grid()
        directions = list(neighbours)
        random.shuffle(directions)

        for direction in directions:
            position = neighbours[direction]
            if position not in visited:
                c_type = maze.get(*position).get_type()
                if direction in ['right', 'left']:
                    if c_type == Type.HORIZONTAL or c_type == Type.EXIT:
                        return position
                elif direction in ['bottom', 'top']: 
                    if c_type == Type.VERTICAL or c_type == Type.EXIT:
                        return position

            # If its not perfect there is 3% chance to break the wall anyway
            elif (not self._is_perfect
                  and random.random() < 0.03
                  and maze.get(*position).get_type() is not Type.ISOLATED):
                return position
        return None

    # Breaks wall between next_pos and carver_cell
    def _break_wall(self, maze, n_x, n_y, x, y):
        if n_y - y == 1:
            maze.get(x, y).bottom_wall = False
        if n_x - x == 1:
            maze.get(x, y).right_wall = False
        if n_y - y == -1:
            maze.get(x, y - 1).bottom_wall = False
        if n_x - x == -1:
            maze.get(x - 1, y).right_wall = False

    # Returns neighbour cells ignoring their type
    def _neighbour_cells(self, maze, x, y):
        neighbours = {}

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
    def _break_frontier(self, maze, visited):
        for inner_pos in visited:
            if maze.get(*inner_pos).get_type() == Type.ISOLATED:
                continue
            neighbours = self._neighbour_cells(maze, *inner_pos)
            for direction, outer_pos in neighbours.items():
                if outer_pos not in visited:
                    visited.add(outer_pos)
                    self._break_wall(maze, *outer_pos, *inner_pos)
                    return outer_pos

    # Adds header to visited to prevent any
    # actions on them
    def _fill_with_unreachable(self, maze, visited):
        for y in range(maze.get_height()):
            for x in range(maze.get_width()):
                if maze.get(x, y).get_type() == Type.ISOLATED:
                    visited.add((x, y))

    def apply(self, maze):
        route = [maze.get_entry()]
        visited = set()
        self._fill_with_unreachable(maze, visited)
        cell_count = maze.get_width() * maze.get_height()

        while len(visited) < cell_count:
            if not route:
                route.append(self._break_frontier(maze, visited))
            carver_pos = route[-1]

            visited.add(carver_pos)
            neighbours = self._neighbour_cells(maze, *carver_pos)
            next_pos = self._next_pos(maze, neighbours, visited)

            if next_pos is None:
                route.pop()
            else:
                self._break_wall(maze, *next_pos, *carver_pos)
                route.append(next_pos)
        return maze
