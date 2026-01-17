#!/usr/bin/env python3

# from maze_generator import Maze
from maze_generator import MazeGenerator
from maze_generator import generation_phases as Phases
from maze_generator import Config
from maze_solver.maze_solver import MazeSolver
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
    generator.add_phase(Phases.AxisPostProcess())
    generator.add_phase(Phases.PathBuildingPhase(is_perfect))

    user_input = None
    while not user_input == 'exit' and not user_input == '4':
        if user_input == '1':
            maze = generator.generate(config)
            print(MazeSolver.shortest_path(maze))
        if user_input == '2':
            maze = generator.generate(config, True)
        if user_input == '3':
            maze = generator.generate(config, True, True)

        user_input = input('''
=== MAZE GENERATOR by afomin and andmarti ===
1. Re-generate
2. Re-generate (display maze, phases)
3. Re-generate (display maze, phases and axis)
4. Exit
Choose action: ''').strip().lower()

else:
    print("[USAGE] python3 main.py {config path} {--random-seed} {seed=}")
