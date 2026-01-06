from maze_generator import Maze
from maze_generator import MazeGenerator
from maze_generator import generation_phases as Phases
from maze_generator import Config
import sys

config_path = "configs/config_all.txt"
config = Config.from_file(config_path)
generator = MazeGenerator()

generator.add_phase(Phases.Add42HeaderPhase())
generator.add_phase(Phases.TypeAssignmentPhase(config.seed))
generator.add_phase(Phases.PathBuildingPhase())

maze = generator.generate(config, True)
