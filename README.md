*This project has been created as part of the 42 curriculum by anrogard and kacherch.*

# A-Maze-ing 🌀

## Description

A-Maze-ing is a procedural maze generator written in Python. Given a configuration file, it generates a random maze, writes it to an output file using a hexadecimal wall-encoding format, and displays it visually in the terminal. The maze can optionally be *perfect* — meaning there is exactly one path between the entry and the exit.

Key features:

- Reproducible generation via a seed
- Perfect maze mode (single path between entry and exit)
- A hidden "42" pattern embedded in the maze using fully-closed cells
- Interactive terminal display: toggle the solution path, change wall colors, regenerate
- A reusable `mazegen` Python package that can be installed via pip

---

## Instructions

### Requirements

- Python 3.10 or later
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

```bash
git clone https://github.com/ROGARD18/A-Maze-ing.git
cd A-Maze-ing
make install
```

### Running the program

```bash
make run
# equivalent to:
poetry run python3 a_maze_ing.py config.txt
```

You can pass a different config file:

```bash
poetry run python3 a_maze_ing.py my_config.txt
```

### Makefile targets

| Target | Description |
|--------|-------------|
| `make install` | Install dependencies via Poetry |
| `make run` | Run the program with the default `config.txt` |
| `make debug` | Run in debug mode (pdb) |
| `make clean` | Remove output file and caches |
| `make lint` | Run flake8 and mypy with standard flags |
| `make lint-strict` | Run flake8 and mypy with `--strict` |

---

## Configuration file format

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are treated as comments and ignored.

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to generate a perfect maze | `PERFECT=True` |

### Optional keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Integer or float seed for reproducibility | `SEED=42` |

### Default `config.txt`

```
WIDTH=9
HEIGHT=9
ENTRY=0,0
EXIT=8,8
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=2
```

---

## Output file format

Each cell is encoded as a single hexadecimal digit representing which walls are closed. Each bit corresponds to a direction:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets the bit to `1`, an open passage sets it to `0`.

Example: `A` (binary `1010`) means the East and West walls are closed.

Cells are written row by row, one row per line. After an empty line, three additional lines follow:
1. Entry coordinates (`x,y`)
2. Exit coordinates (`x,y`)
3. Shortest path from entry to exit using `N`, `E`, `S`, `W`

---

## Maze generation algorithm

This project uses the **recursive backtracker** algorithm (also known as depth-first search with backtracking).

**How it works:**

1. Start at a random cell, mark it as visited.
2. Randomly choose an unvisited neighbor, remove the wall between them, and recurse.
3. If no unvisited neighbors remain, backtrack to the previous cell.
4. Repeat until all cells have been visited.

**Why this algorithm?**

The recursive backtracker produces mazes with long, winding corridors and relatively few dead ends, which makes it visually interesting and gives a satisfying feel to the "42" pattern. It natively produces a *perfect* maze (a spanning tree of the grid), satisfying the `PERFECT=True` constraint without additional post-processing. It is also simple to implement, easy to reason about, and efficient enough for the maze sizes required by this project.

---

## Visual representation

The program offers an interactive terminal display with the following controls:

1. **Re-generate** a new maze with a fresh random seed
2. **Show/Hide** the shortest path from entry to exit
3. **Rotate wall colors** through a preset palette
4. **Quit**

The display clearly marks the entry (colored cell), the exit (colored cell), walls, open passages, and — when toggled — the solution path highlighted in a distinct color.

The maze always includes a visible **"42"** pattern composed of fully-closed cells. If the maze is too small to fit the pattern, a message is printed to the console.

---

## Reusable module — `mazegen`

The maze generation logic is packaged as a standalone Python package called `mazegen`, located in the `mazegen/` directory.

### Installation

From the root of the repository, in a virtual environment:

```bash
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

Or install directly from source:

```bash
pip install .
```

### Basic usage

```python
from mazegen import MazeGenerator

# Instantiate with custom parameters
gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)

# Generate the maze
gen.generate()

# Access the maze grid
grid = gen.maze  # 2D list of cells, each cell is an int (hex wall bitmask)

# Access the solution (list of directions: 'N', 'E', 'S', 'W')
path = gen.solve(entry=(0, 0), exit=(19, 14))
print("Shortest path:", path)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `seed` | `int \| float \| None` | Random seed for reproducibility |
| `perfect` | `bool` | If `True`, generates a perfect maze |

### Accessing the structure

- `gen.maze` — 2D list of integers (one per cell), where each integer encodes walls as a 4-bit bitmask (N=bit0, E=bit1, S=bit2, W=bit3).
- `gen.solve(entry, exit)` — Returns the shortest path as a list of direction characters.

> Note: the internal maze structure uses a bitmask per cell, which is the same format as the output file.

---

## Team and project management

### Team members

| Member | Role |
|--------|------|
| anrogard | Sole developer — architecture, generation algorithm, visual display |
| kacherch | Sole developer — architecture, generation algorithm, packaging |

### Planning

The project was initially scoped as a two-week sprint:

In practice, the constraint-satisfaction logic for the "42" pattern and the open-area restriction (no 3×3 open zones) required more iteration than anticipated, shifting the timeline slightly. The packaging step was completed last and proved straightforward with `setuptools` and `pyproject.toml`.

### What worked well

- The recursive backtracker was a natural fit for the perfect maze requirement and produced clean, explorable mazes immediately.
- Using `pydantic` for config validation caught bad inputs early with clear error messages.
- Separating the generation logic into a standalone `mazegen` package from the start made the final packaging step trivial.

### What could be improved

- Adding support for multiple generation algorithms (Prim's, Kruskal's) as a bonus.
- A graphical display using MiniLibX instead of — or in addition to — the terminal renderer.
- More comprehensive unit tests for edge cases (1×1 maze, entry == exit border cases).

### Tools used

- **Poetry** — dependency management and virtual environments
- **pydantic** — config validation with type safety
- **flake8 + mypy** — linting and static type checking
- **Claude (Anthropic)** — used for generating documentation drafts and README structure, then reviewed and adapted manually

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explained — think-maths.co.uk](https://www.think-maths.co.uk/maze)
- [Spanning trees and perfect mazes — astrolog.org](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Python type hints — PEP 484](https://peps.python.org/pep-0484/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [pydantic documentation](https://docs.pydantic.dev/)

### AI usage

AI was used to assist with:
- Drafting and structuring this README