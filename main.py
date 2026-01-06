from maze_generator import Maze
from maze_generator import MazeGenerator
from maze_generator import TypeAssignmentPhase, Add42HeaderPhase
from maze_generator import Config
import sys

generator = MazeGenerator()

generator.add_phase(Add42HeaderPhase())
generator.add_phase(TypeAssignmentPhase())
#generator.add_phase(PathBuildingPhase())
#generator.add_phase(OnizukaPhase())

if len(sys.argv) >= 3:
    width = int(sys.argv[1])
    height = int(sys.argv[2])
else:
    width = 7
    height = 5

maze = generator.generate(width, height, True, True)

