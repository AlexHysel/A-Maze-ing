#afomin

from .models import Maze
from .generation_phases import GenerationPhase
from .config import Config


class MazeGenerator():
    def __init__(self):
        self.__phases = []

    def add_phase(self, phase: GenerationPhase):
        if isinstance(phase, GenerationPhase):
            self.__phases.append(phase)
        else:
            raise Exception("[ERROR] All generation phases should be" +
                  "subclasses of GenerationPhase.")

    def generate(self, config: Config, log=False):
        maze = Maze(config.width, config.height)
        maze.get(*config.entry_pt).set_type(3)
        maze.get(*config.exit_pt).set_type(4)
        for phase_id, phase in enumerate(self.__phases):
            maze = phase.apply(maze, log, phase_id)
        return maze
