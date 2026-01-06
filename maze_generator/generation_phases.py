#afomin

from abc import ABC, abstractmethod
from .maze_display import MazeRenderer
from .models import Type
import random


def log_phase(func):
    def wrapper(self, maze, log, phase_id):
        if log:
            print(f'[PHASE {phase_id}] {self.__class__.__name__} started.')
        
        #try:
            result = func(self, maze, log, phase_id)

        #except Exception as e:
        #    print(f'[PHASE {phase_id}]', e)

        #else:
        #    if log:
        #        print(f'[PHASE {phase_id}] Finished successfully.')
        #        MazeRenderer.display(result, True)
            return result

    return wrapper


# === Basic phase ===

class GenerationPhase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, maze, log, phase_id):
        pass


# === Phases ===

class Add42HeaderPhase(GenerationPhase):
    @log_phase
    def apply(self, maze, log, phase_id):
        h = maze.get_height()
        w = maze.get_width()
        if h >= 5 and w >= 7:
            x = int(w / 2 - 3.5)
            y = int(h / 2 - 2.5)
            #4
            maze.get(x, y).set_type(2)
            maze.get(x, y + 1).set_type(2)
            maze.get(x, y + 2).set_type(2)
            maze.get(x + 1, y + 2).set_type(2)
            maze.get(x + 2, y + 2).set_type(2)
            maze.get(x + 2, y + 3).set_type(2)
            maze.get(x + 2, y + 4).set_type(2)
            #2
            maze.get(x + 4, y).set_type(2)
            maze.get(x + 5, y).set_type(2)
            maze.get(x + 6, y).set_type(2)
            maze.get(x + 6, y + 1).set_type(2)
            maze.get(x + 4, y + 2).set_type(2)
            maze.get(x + 5, y + 2).set_type(2)
            maze.get(x + 6, y + 2).set_type(2)
            maze.get(x + 4, y + 3).set_type(2)
            maze.get(x + 4, y + 4).set_type(2)
            maze.get(x + 5, y + 4).set_type(2)
            maze.get(x + 6, y + 4).set_type(2)

        elif log:
            print(f'Cencelled, maze less than 5x7.')
        return maze


class TypeAssignmentPhase(GenerationPhase):
    def __init__(self, seed = None):
        if seed is not None:
            random.seed(seed)

    @log_phase
    def apply(self, maze, log, phase_id):
        for row in maze.get_grid():
            for cell in row:
                if cell.get_type() is None:
                    cell.set_type(random.randint(0, 1))
        return maze


class PathBuildingPhase(GenerationPhase):
    def _next_cell(self, maze, neighbours, visited):
        grid = maze.get_grid()

        for direction, position in neighbours.items():
            if position not in visited:
                cell_type = maze.get(*position).get_type()
                if direction in ['right', 'left'] and cell_type == Type.HORIZONTAL:
                    return position
                if direction in ['bottom', 'top'] and cell_type == Type.VERTICAL:
                    return position
        return None

    def _break_wall(self, maze, n_x, n_y, x, y):
        if n_y - y == 1:
            maze.get(x, y).bottom_wall = False
        if n_x - x == 1:
            maze.get(x, y).right_wall = False
        if n_y - y == -1:
            maze.get(x, y - 1).bottom_wall = False
        if n_x - x == -1:
            maze.get(x - 1, y).right_wall = False

    def _neighbour_cells(self, maze, x, y):
        neighbours = {}
        w = maze.get_width()
        h = maze.get_height()

        if y + 1 < h:
            neighbours['bottom'] = (x, y + 1)
        if x + 1 < w:
            neighbours['right'] = (x + 1, y)
        if y - 1 >= 0:
            neighbours['top'] = (x, y - 1)
        if x - 1 >= 0:
            neighbours['left'] = (x - 1, y)

        return neighbours

    @log_phase
    def apply(self, maze, log: bool, phase_id: int):
        route = [maze.get_entry()]
        visited = set()
        cell_count = maze.get_width() * maze.get_height()

        while len(visited) < cell_count:
            if len(route) == 0:
                found = False
                for y, row in enumerate(maze.get_grid()):
                    for x, cell in enumerate(row):
                        if (x, y) not in visited:
                            neighbours = self._neighbour_cells(maze, x, y).values()
                            for neighbour in neighbours:
                                if neighbour in visited:
                                    self._break_wall(maze, *neighbour, x, y)
                                    route.append(neighbour)
                                    found = True       
                                    break
                        if found:
                            break
                    if found:
                        break

            curr_cell = route[-1]

            MazeRenderer.display(maze, True)

            visited.add(curr_cell)
            neighbours = self._neighbour_cells(maze, *curr_cell)
            next_cell = self._next_cell(maze, neighbours, visited)

            if next_cell is None:
                route.pop()
            else:
                self._break_wall(maze, *next_cell, *curr_cell)
                route.append(next_cell)
        return maze
