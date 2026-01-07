#afomin

from .models import Maze
from .generation_phases import GenerationPhase
from .maze_display import MazeRenderer
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
        maze = Maze(config.width, config.height, config.entry_pt, config.exit_pt)
        for phase_id, phase in enumerate(self.__phases):
            if log:
                print(f'[PHASE {phase_id}]', phase.get_start_message())
            maze = phase.apply(maze)
            if log:
                print(f'[PHASE {phase_id}]', phase.get_finish_message())
                MazeRenderer.display(maze, False)
        return maze
