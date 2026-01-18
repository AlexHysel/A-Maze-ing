#!/usr/bin/env python3

from maze_generator import MazeGenerator
from maze_generator import MazeRenderer
from maze_generator import generation_phases as Phases
from maze_generator import Config
from MazeSolver.maze_solver import MazeSolver
import sys
import os

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

    renderer = MazeRenderer()

    user_input: str | None = None
    path: list[tuple[int, int]] | None = None
    show_path = False

    maze = generator.generate(config)
    while user_input not in ['quit', '5']:
        user_input = input('''=== A-Maze-ing by afomin and andmarti ===
1. Re-generate a new maze
2. Re-generate a new maze (log phases)
3. Show/Hide path from entry to exit
4. Rotate maze colors
5. Quit
Choice? (1-4): ''').strip()
        os.system('clear')

        if user_input == '1':
            maze = generator.generate(config)
            path = MazeSolver.shortest_path(maze)

        elif user_input == '2':
            maze = generator.generate(config, renderer)
            path = MazeSolver.shortest_path(maze)

        elif user_input == '3':
            show_path = not show_path

        elif user_input == '4':
            renderer.rotate_color()

        else:
            print('Unknown command.')
            continue

        renderer.display(maze, path=path, show_path=show_path)
        renderer.save_formatted_output(maze, path, config.output_file)

else:
    print("[USAGE] python3 main.py {config path} {--random-seed} {seed=}")
