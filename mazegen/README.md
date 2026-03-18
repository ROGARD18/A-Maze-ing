# mazegen — Documentation

`mazegen` is a Python package for procedural maze generation and solving. It exposes a simple `MazeGenerator` class that handles maze creation, structure access, and pathfinding.

---

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or install from source in a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install build
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

---

## Quick Start

```python
from mazegen.generator import MazeGenerator
from mazegen.models import Config

# 1. Create a Config object
config = Config(
    width=21,
    height=15,
    entry_x=0,
    entry_y=0,
    exit_x=20,
    exit_y=14,
    output_file="maze.txt",
    perfect=True,
    algorithm="kruskal",
    seed=None,
)

# 2. Instantiate the generator
generator = MazeGenerator(
    config=config,
    algorithm="kruskal",
    color="\u001b[0;36m",   # cyan walls
    color_42="\u001b[0;35m", # magenta for the "42" zone
    gen_time=0.0,            # no animation delay
)

# 3. Access the maze grid
grid = generator.grid

# 4. Solve the maze
path, directions = generator.solve()
print("Direction string:", directions)  # e.g. "SSSEEENNE..."
```

---

## Custom Parameters

All parameters are passed through the `Config` object:

| Parameter     | Type           | Description                                              | Constraints               |
|---------------|----------------|----------------------------------------------------------|---------------------------|
| `width`       | `int`          | Number of columns in the maze                            | 9 ≤ width ≤ 1000          |
| `height`      | `int`          | Number of rows in the maze                               | 7 ≤ height ≤ 1000         |
| `entry_x`     | `int`          | X coordinate of the entry cell                           | 0 ≤ entry_x < width       |
| `entry_y`     | `int`          | Y coordinate of the entry cell                           | 0 ≤ entry_y < height      |
| `exit_x`      | `int`          | X coordinate of the exit cell                            | 0 ≤ exit_x < width        |
| `exit_y`      | `int`          | Y coordinate of the exit cell                            | 0 ≤ exit_y < height       |
| `output_file` | `str`          | Path of the output file (must end in `.txt`)             | 5–30 characters           |
| `perfect`     | `bool`         | If `True`, generates a perfect maze (no loops)           | —                         |
| `algorithm`   | `str`          | Generation algorithm to use                              | `"kruskal"`|
| `seed`        | `float \| None` | Random seed for reproducibility; `None` = random         | Optional                  |

### Reproducible maze with a seed

```python
config = Config(
    width=15, height=11,
    entry_x=0, entry_y=0,
    exit_x=14, exit_y=10,
    output_file="maze.txt",
    perfect=True,
    algorithm="kruskal",
    seed=42.0,   # <-- fixed seed
)
```

### Imperfect maze (with loops)

```python
config = Config(
    ...,
    perfect=False,  # extra walls will be broken to create multiple paths
)
```

---

## Accessing the Generated Structure

After instantiation, `MazeGenerator` exposes:

### `generator.grid` — the full maze

`grid` is a `Grid` (i.e. `list[list[Cell]]`). Each `Cell` has the following attributes:

| Attribute  | Type   | Description                                          |
|------------|--------|------------------------------------------------------|
| `x`        | `int`  | Column index                                         |
| `y`        | `int`  | Row index                                            |
| `north`    | `int`  | `1` = wall present, `0` = passage                   |
| `south`    | `int`  | `1` = wall present, `0` = passage                   |
| `east`     | `int`  | `1` = wall present, `0` = passage                   |
| `west`     | `int`  | `1` = wall present, `0` = passage                   |
| `is_entry` | `bool` | `True` if this cell is the entry point               |
| `is_exit`  | `bool` | `True` if this cell is the exit point                |
| `in_path`  | `bool` | `True` if this cell is part of the solution path     |
| `set_id`   | `int`  | Internal set identifier used during generation       |

```python
# Access a specific cell
cell = generator.grid[y][x]
print(cell.north, cell.east, cell.south, cell.west)  # wall values
```

> **Note:** the grid format is `grid[row][col]`, i.e. `grid[y][x]`.

---

## Solving the Maze

```python
path, directions = generator.solve()
```

`solve()` returns a tuple:

- `path` — `list[Cell]`: the ordered list of cells from entry to exit.
- `directions` — `str`: a compact string of cardinal moves (`N`, `S`, `E`, `W`).

```python
path, directions = generator.solve()

print(f"Solution length: {len(path)} steps")
print(f"Directions: {directions}")

# Iterate over solution cells
for cell in path:
    print(f"  ({cell.x}, {cell.y})")
```

The result is cached: calling `solve()` multiple times on the same instance is free.

---

## Displaying the Maze

```python
from mazegen.generator import MazeGenerator

MazeGenerator.draw_maze(
    maze=generator.grid,
    config=config,
    color="\u001b[0;36m",
    color_42="\u001b[0;35m",
    path=path,           # pass None to display without solution
)
```

This renders the maze in the terminal using Unicode block characters. The solution path is highlighted in white, the entry in yellow, and the exit in red.

---

## Saving to File

```python
generator.create_output_file(path=directions)
```

This writes the maze to the file specified in `config.output_file`. The format encodes each cell's wall configuration as a hex character (`0`–`F`), followed by the entry/exit coordinates and the direction string.

---

## Available Algorithms

| Name       | Description                                      |
|------------|--------------------------------------------------|
| `kruskal`  | Randomized Kruskal's algorithm (spanning tree)   |

---

## The "42" Zone

All mazes contain a reserved zone in the center shaped like the number **42**. Cells in this zone are fully walled and inaccessible. Entry and exit points cannot be placed inside this zone.

---

## Full Example

```python
from mazegen.generator import MazeGenerator
from mazegen.models import Config

config = Config(
    width=31,
    height=21,
    entry_x=0,
    entry_y=0,
    exit_x=30,
    exit_y=20,
    output_file="output.txt",
    perfect=True,
    algorithm="kruskal",
    seed=3.14,
)

gen = MazeGenerator(
    config=config,
    algorithm="kruskal",
    color="\u001b[0;36m",
    color_42="\u001b[0;35m",
    gen_time=0.0,
)

path, directions = gen.solve()
print("Solved in", len(path), "steps:", directions)

MazeGenerator.draw_maze(gen.grid, config, "\u001b[0;36m", "\u001b[0;35m", path)
gen.create_output_file(directions)
```