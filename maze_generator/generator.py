from .models import Maze
from .generation_phases import GenerationPhase


class MazeGenerator():
    def __init__(self):
        self.__phases = []

    def add_phase(self, phase: GenerationPhase):
        if isinstance(phase, GenerationPhase):
            self.__phases.append(phase)
        else:
            raise Exception("[ERROR] All generation phases should be" +
                  "subclasses of GenerationPhase.")

    def generate(self, width, height, is_perfect, log=False):
        maze = Maze(width, height)
        maze.get(0, 0).set_type(3)
        maze.get(width - 1, height - 1).set_type(4)
        for phase_id, phase in enumerate(self.__phases):
            maze = phase.apply(maze, log, phase_id)
        return maze
