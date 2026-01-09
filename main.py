from maze_generator import Maze
from maze_generator import MazeGenerator
from maze_generator import generation_phases as Phases
from maze_generator import Config
import sys

if (len(sys.argv) > 1):
    config_path = sys.argv[1].strip()
    config = Config.from_file(config_path)

    seed = config.seed
    is_perfect = config.is_perfect
    
    for arg in sys.argv[1:]:
        if 'seed=' in arg:
            seed = int(arg[5:])
        elif arg == '--random-seed':
            seed = None

    generator = MazeGenerator()

    generator.add_phase(Phases.Add42HeaderPhase())
    generator.add_phase(Phases.TypeAssignmentPhase(seed))
    generator.add_phase(Phases.PathBuildingPhase(is_perfect))

    maze = generator.generate(config, True)

else:
    print("[USAGE] python3 main.py {config path} {--random-seed} {seed=}")
