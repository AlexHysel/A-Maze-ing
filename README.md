
# A-Maze-ing Generator

*This project has been created as part of the 42 curriculum by afomin, andmarti.*

## Description

**A-Maze-ing** is a procedural maze generation engine built with a focus on control and determinism. Unlike traditional randomized generators, this project implements a **Field-Constrained Deterministic Backtracker**.

The goal was to create a generator where the "flow" of the maze is guided by an underlying vector field, allowing developers to influence the maze's aesthetic while maintaining a solvable, single-path (or braid) structure.

## Instructions

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/A-Maze-ing.git
cd 42-A-Maze-ing

```


2. Install dependencies (e.g., Colorama):
```bash
pip install -r requirements.txt

```



### Execution

Run the generator using:

```bash
python main.py configs/config_all.txt (Optional: seed=[any number], --random-seed)

```

### Documentation

Here's ***Maze*** class __init__ params:

```Python
 36 class Maze:
 37     def __init__(
 38         self,
 39         width: int,
 40         height: int,
 41         entry_pt: tuple[int, int],
 42         exit_pt: tuple[int, int],
 43         grid: list[list[Cell]] | None = None
 44     ) -> None:
```

Here are some methods of Maze class:

```Python
def get_cell(self, x: int, y: int) -> Cell
def get_hex_of_cell(self, x: int, y: int) -> str
```

Maze contains ***Cell*** objects:

```Python
 16 class Cell:
 17     def __init__(
 18             self,
 19             bottom_wall = True,
 20             right_wall = True
 21     ) -> None:
```

They can be one of these types (For generation):

```Python
  6 class CellType(Enum):
  7     NOTYPE = 0
  8     HORIZONTAL = 1
  9     VERTICAL = 2
 10     ISOLATED = 3
 11     ENTRY = 4
 12     EXIT = 5

```

We have ***MazeGenerator*** which is used to create mazes. It is a pipeline that creates simple maze and applies ***Generation Phases*** you added.

Here's how to pass params. If you added Renderer it will use it to show your output

```Python 
def generate(self, config: Config, renderer: MazeRenderer = None)
```

```Python
generator = MazeGenerator() # Creating generator
generator.add_phase(Phases.TypeAssignmentPhase(seed)) # Adding phase
maze = generator.generate(config) # Create maze using config object
```

Here is basic abstract class for Generation Phases, which you can use to write you own using inheritance.
Every phase takes maze object (that was created in generator.generate(config)), changes it and returnes updated version.

```Python
 10 class GenerationPhase(ABC):
 11     _GREEN = '\033[92m'
 12     _YELLOW = '\033[93m'
 13     _RED = '\033[91m'
 14     _RESET = '\033[0m'
 15 
 16     def __init__(self) -> None:
 17         self._start_message: str = f'{self.__class__.__name__} started.'
 18         self._finish_message: str = f'{self.__class__.__name__} finished.'
 19 
 20     @abstractmethod
 21     def apply(self, maze: Maze): # Method that will be polymorphically used to create maze.
 22         pass
 23 
 24     def get_start_message(self): # Returns message on phase start to print it in log
 25         return self._start_message
 26 
 27     def get_finish_message(self): # Returns message on phase finish to print it in log. You can change it on exceptions catch, to show error message
 28         return self._finish_message

```

You also can use this method to get the path.

```Python
  5 class MazeSolver():
  6     @staticmethod
  7     def shortest_path(maze: Maze) -> list[tuple[int, int]]:
```

## Config File Structure

The generator uses a configuration file to define the generation parameters. Below is the example:

```
WIDTH=16
HEIGHT=16
ENTRY=0, 0
EXIT=13, 12
OUTPUT_FILE=maze_all.txt
PERFECT=False
SEED=42
```

## Technical Choices

### The Algorithm: Field-Constrained Deterministic Backtracker

I created a simple algorithm that creates maze with isoleted cells, assigns random axises to all of them and then uses carver to carve the path.
MazeGenerator class works like pipeline and contains list of GenerationPhase subclasses and applies them all one by one (You can see them 
using '2. Re-generate a new maze (log phases)')
Here are basic phases:

0. **Phase 0: 42 Header**: Place 42 if maze is 7x5 or bigger and header doesnt collide with entry and exit points
1. **Phase 1: Axis Assignment**: A grid of vectors is generated (Noise Field).
2. **Phase 2: Axis Correction**: The field is processed to ensure logical flow.
3. **Phase 3: Carving Path**: A backtracking agent moves through the grid. At each cell, it prioritizes directions based on the underlying vector field but uses a **Seeded Shuffle** for its secondary choices to prevent "teeth" artifacts.

Why this algorithm: Its deterministic and using vector field allows to add different phases to change this field or create 
it using other algorithm which will cause different results.

## Reusability

The following components are designed to be modular:

* **`GenerationPhase` (ABC)**: An abstract base class that allows you to plug in new generation steps (e.g., a "Room Placer" or "Treasure Spawner") without changing the core engine.
* **Colorized Terminal Output**: The logic for using ANSI background colors to visualize grids is independent of the maze logic.

## Team and Project Management

* **Roles**:
* **afomin**: Algorithm, Generation Phases, MazeSolver and code architecture.
* **andmarti**: Output to file and terminal, vector field correction phase, config, Makefile, linting and packaging.


* **Planning & Evolution**:
* *Initial Plan*: Use simple recursive backtracker.
* *Evolution*: Moved to a phase-based system to solve the "parallel corridor" problem and allow for more artistic control.


* **Retrospective**:
* *What worked well*: The separation of the `Carver` from the `NoiseField` allowed us to work on the logic and the "look" of the maze simultaneously.
* *Improvements*: Improve non-perfect maze generation.


* **Tools**:
* Python 3
* Git/GitHub for version control



## Resources

* **Documentation**: Python `enum` and `random` documentation.

* **AI Usage**: AI was used as a **thought partner** for:
* Debugging Errors.
* Writing basic README.
