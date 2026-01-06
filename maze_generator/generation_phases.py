#afomin

from abc import ABC, abstractmethod
from .maze_display import MazeRenderer
from .models import Type
import random


def log_phase(func):
    def wrapper(self, maze, log, phase_id):
        if log:
            print(f'[PHASE {phase_id}] {self.__class__.__name__} started.')
        
        try:
            result = func(self, maze, log, phase_id)

        except Exception as e:
            print(f'[PHASE {phase_id}]', e)

        else:
            if log:
                print(f'[PHASE {phase_id}] Finished successfully.')
                MazeRenderer.display(result, True)
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
    def _get_directions(self, maze, x, y):
        grid = maze.get_grid()
        directions = {}

        if y + 1 < maze.get_height():
            directions['bottom'] = grid[y + 1][x].get_type() == Type.VERTICAL
        else:
            directions['bottom'] = False

        if x + 1 < maze.get_width():
            directions['right'] = grid[y][x + 1].get_type() == Type.HORIZONTAL
        else:
            directions['right'] = False
        if y - 1 >= 0:
            directions['top'] = grid[y - 1][x].get_type() == Type.VERTICAL
        else:
            directions['top'] = False

        if x - 1 >= 0:
            directions['left'] = grid[y][x - 1].get_type() == Type.HORIZONTAL
        else:
            directions['left'] = False

        return directions 

    def _break_near_walls(self, directions, maze, x, y):
        if directions['bottom']:
            maze.get(x, y).bottom_wall = False
        if directions['right']:
            maze.get(x, y).right_wall = False
        if directions['top']:
            maze.get(x, y - 1).bottom_wall = False
        if directions['left']:
            maze.get(x - 1, y).right_wall = False

    def _move(self, direction: str, x, y):
        if direction == 'bottom':
            return (x, y + 1)
        if direction == 'right':
            return (x + 1, y)
        if direction == 'top':
            return (x, y - 1)
        if direction == 'left':
            return (x - 1, y)

    @log_phase
    def apply(self, maze, log, phase_id):
        x, y = maze.get_entry()

        for i in range(10):
            directions = self._get_directions(maze, x, y)
            self._break_near_walls(directions, maze, x, y) 
            for key in ['bottom', 'right', 'top', 'left']:
                if directions[key]:
                    x, y = self._move(key, x, y)
                    break
        return maze


class OnizukaPhase(GenerationPhase):
    @log_phase
    def apply(self, maze, log, phase_id):
        return maze
