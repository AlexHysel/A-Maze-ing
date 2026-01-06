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
            print(f'[PHASE {phase_id}]:', e)

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
    @log_phase
    def apply(self, maze, log, phase_id):
        for row in maze.get_grid():
            for cell in row:
                if cell.get_axis() is None:
                    cell.set_type(random.randint(0, 1))
        return maze


class PathBuildingPhase(GenerationPhase):
    @log_phase
    def apply(self, maze, log, phase_id):
        return maze


class OnizukaPhase(GenerationPhase):
    @log_phase
    def apply(self, maze, log, phase_id):
        return maze
