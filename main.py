from maze_generator import Maze
from maze_generator import MazeGenerator
from maze_generator import TypeAssignmentPhase, Add42HeaderPhase
from maze_generator import Config
import sys

config_path = input()
config_path = "configs/" + config_path
config = Config.from_file(config_path)
generator = MazeGenerator()

generator.add_phase(Add42HeaderPhase())
generator.add_phase(TypeAssignmentPhase())
#generator.add_phase(PathBuildingPhase())
#generator.add_phase(OnizukaPhase())

maze = generator.generate(config, True)

