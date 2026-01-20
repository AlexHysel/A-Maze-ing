
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
* **andmarti**: Output to file and terminal, vector field correction phase, config, Makefile.


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
