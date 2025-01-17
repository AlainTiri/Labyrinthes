
# README

## Maze Generation and Visualization Project

This project implements a **maze generation and visualization tool** in Python. It provides functionalities to generate mazes of different shapes and sizes, explore them, and save them as a PDF file. The goal of this tool is to programmatically create mazes, either rectangular or circular, and optionally visualize and export their solutions.

---

## Features

- **Maze Generation**:
  - Create mazes of various sizes and difficulty levels.
  - Supports two shapes: `rectangular` and `circle`.
  
- **Maze Exploration**:
  - Implements **depth-first search (DFS)** to generate maze paths.
  - Explore the maze to mark visited paths.

- **Visualization**:
  - Display the generated maze visually using **Matplotlib**.
  - Start and end points of the maze are displayed with markers.
  
- **Export to PDF**:
  - Save multiple mazes of the same configuration into a PDF file for easy distribution or printing.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AlainTiri/Labyrinthes
   cd Labyrinthes
   ```

2. **Install Required Libraries**:
   Make sure to install the required Python libraries. You can use `pip` to install them:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

The project provides both a direct script usage and reusable classes for creating and working with mazes.

### Generating Mazes
To create and save mazes to a file, you can run the script:
```bash
python maze.py
```

### Example Parameters
You can configure the script by modifying:
- Number of mazes (`nbr_mazes`)
- Difficulty level (`difficulty`) from 1 to 9.
- Shape of the maze (`figure`) which can be `"rectangular"` or `"circle"`.

Example configuration:
```python
nombre_labyrinthes = 24
difficulty = 3
figure = "rectangular"
```

### Program Output
After running the script, the generated mazes will be saved to a PDF:
```bash
24 mazes circle of difficulty 3 had been saved into file.
```

### Generating Mazes Programmatically
You can create and display a maze by using the `creation()` function:

```python
from maze import creation

maze = creation(10, 10, "rectangular")  # 10x10 rectangular maze
maze.show()
```

---

## Project Structure

- **`Stack` Class**:
  - Implements a basic stack for DFS-based exploration.

- **`MazeCell` Class**:
  - Represents individual cells in the maze and stores information about walls and visited status.

- **`Maze` Class**:
  - Creates a maze grid with cells and supports visualization methods.

- **Key Functions**:
  - `creation(p, q, fig)`: Creates a maze of given dimensions and shape.
  - `explore(maze)`: Explores the maze and provides a solution path.
  - `to_pdf(filename, level, n, fig, difficulty)`: Saves `n` mazes into a PDF file.

---

## Requirements

- **Python**: >= 3.8
- **Packages**:
  - `numpy`
  - `matplotlib`

---

## Examples

### Generate and Show a Maze
```python
# Import and generate a maze
from maze import creation

maze = creation(15, 10, "rectangle")  # Generate a 15x10 rectangular maze
maze.show()                           # Display the maze
```

### Export Multiple Mazes to PDF
```python
from maze import to_pdf

level = {"rows": 20, "columns": 15}       # Define maze dimensions
to_pdf("mazes.pdf", level, 10, "circle", 3)  # Save 10 circular mazes of difficulty 3
```

---

## Shape Overview

Maze generation supports two shapes:
- **Rectangle**: Standard grid-based mazes.
- **Circle**: Circular mazes with excluded cells outside the radius.

### Example Visualizations

- **Rectangular Maze**:
  ```
  +---+---+---+
  |   |       |
  +---+   +---+
  |       |   |
  +---+---+---+
  ```

- **Circular Maze**:
  ```
  A labyrinth displayed in a circular pattern with valid cells forming a circle.
  ```

---

## Contribution

Contributions are welcome! Feel free to open issues or pull requests.

### To Contribute:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or issues, feel free to contact Alain Tiri or open a GitHub issue.
