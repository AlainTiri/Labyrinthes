from numpy.random import randint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class Stack:
    def __init__(self):
        """Initialize an empty stack."""

        self.items = []

    def is_empty(self):
        """Check if the stack is empty."""

        return self.items == []

    def push(self, item):
        """Push an item onto the stack."""

        self.items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():

            raise ValueError("Stack is empty")

        return self.items.pop()


class MazeCell:
    """Represents a cell in the maze with walls in four directions and a visited status."""
    def __init__(self):
        self.N = False
        self.W = False
        self.S = False
        self.E = False
        self.visited = False


def explore(maze):
    """Explore the maze from the start to the end, marking visited cells."""
    stack = Stack()
    stack.push((0, maze.columns - 1))
    maze.grid[0][maze.columns - 1].visited = False
    while True:
        i, j = stack.pop()
        if i == maze.rows - 1 and j == 0:
            break
        if j > 0 and maze.grid[i][j].S and maze.grid[i][j - 1].visited:
            stack.push((i, j))
            stack.push((i, j - 1))
            maze.grid[i][j - 1].visited = False
        elif i < maze.rows - 1 and maze.grid[i][j].E and maze.grid[i + 1][j].visited:
            stack.push((i, j))
            stack.push((i + 1, j))
            maze.grid[i + 1][j].visited = False
        elif j < maze.q - 1 and maze.grid[i][j].N and maze.grid[i][j + 1].visited:
            stack.push((i, j))
            stack.push((i, j + 1))
            maze.grid[i][j + 1].visited = False
        elif i > 0 and maze.grid[i][j].W and maze.grid[i - 1][j].visited:
            stack.push((i, j))
            stack.push((i - 1, j))
            maze.grid[i - 1][j].visited = False
    return stack.items

class Maze:
    """Represents a maze with cells, supporting various shapes."""

    def __init__(self, rows, columns, shape="rectangle"):

        self.rows = rows
        self.columns = columns
        self.grid = [[MazeCell() for j in range(columns)] for i in range(rows)]
        self.shape = shape
        self.valid_cells = self._generate_valid_cells()

    def _generate_valid_cells(self):
        """Generate a matrix indicating valid cells based on the labyrinth shape."""
        valid = np.ones((self.rows, self.columns), dtype=bool)
        if self.shape == "circle":
            cx, cy = self.rows // 2, self.columns // 2
            radius = min(self.rows, self.columns) // 2
            for i in range(self.rows):
                for j in range(self.columns):
                    if (i - cx) ** 2 + (j - cy) ** 2 > radius ** 2:
                        valid[i, j] = False
        return valid

    def canvas(self):
        start_line = randint((self.columns) / 2) + round(self.columns / 2)
        end_line = randint(self.columns / 2)
        lw = 4

        # interior borders
        for i in range(self.rows - 1):
            for j in range(self.columns):
                if not self.grid[i][j].E and self.valid_cells[i, j] and self.valid_cells[i + 1, j]:
                    plt.plot([i + 1, i + 1], [j, j + 1], 'b', linewidth=lw)
        for j in range(self.columns - 1):
            for i in range(self.rows):
                if not self.grid[i][j].N and self.valid_cells[i, j] and self.valid_cells[i, j + 1]:
                    plt.plot([i, i + 1], [j + 1, j + 1], 'b', linewidth=lw)

        # Parcours chaque cellule
        for i in range(self.rows):
            for j in range(self.columns):
                if not self.valid_cells[i, j]:
                    continue  # Ignore les cellules non valides

                # Vérifie les bordures et dessine les murs manquants
                # Ouest (gauche)
                if i == 0 or not self.valid_cells[i - 1, j]:
                    if j == start_line:
                        plt.plot(i - 0.5, j + 0.5, marker='o', color='green', markersize=9, label='Start',
                                 solid_capstyle="round")
                    else:
                        plt.plot([i, i], [j, j + 1], 'b', linewidth=lw + 1, solid_capstyle="round")  # Mur gauche

                # Est (droite)
                if i == self.rows - 1 or i + 1 >= self.rows or not self.valid_cells[i + 1, j]:
                    if j == end_line:
                        plt.plot(i + 1.5, j + 0.5, marker='*', color='red', markersize=9, label='End',
                                 solid_capstyle="round")
                    else:
                        plt.plot([i + 1, i + 1], [j, j + 1], 'b', linewidth=lw + 1, solid_capstyle="round")  # Mur droit

                # Sud (bas)
                if j == 0 or not self.valid_cells[i, j - 1]:
                    plt.plot([i, i + 1], [j, j], 'b', linewidth=lw + 1, solid_capstyle="round")  # Mur bas

                # Nord (haut)
                if j == self.columns - 1 or not self.valid_cells[i, j + 1]:
                    plt.plot([i, i + 1], [j + 1, j + 1], 'b', linewidth=lw + 1, solid_capstyle="round")  # Mur haut

        plt.axis('off')

    def solution_path(self):
        path = explore(self)
        X, Y = [], []
        for (i, j) in path:
            X.append(i + .5)
            Y.append(j + .5)
        X.append(self.rows - .5)
        Y.append(.5)
        plt.plot(X, Y, 'r', linewidth=2)

    def show(self):
        self.canvas()
        plt.show()


def creation(p, q, fig="rectangle"):
    """
    Generate a maze of size p x q and shape `fig`.

    This function initializes a maze and generates valid paths within it.
    It ensures that the maze follows the specified shape and that valid paths
    connect all cells according to rules of the maze generation algorithm.

    Parameters:
        p (int): Number of rows in the maze.
        q (int): Number of columns in the maze.
        fig (str): Shape of the maze, either "rectangle" or "circle".

    Returns:
        Maze: A generated maze object with proper walls set up.
    """
    maze = Maze(p, q, fig)
    pile = Stack()
    while True:
        i, j = randint(p), randint(q)
        if maze.valid_cells[i, j]:
            break
    pile.push((i, j))
    maze.grid[i][j].visited = True
    while not pile.is_empty():
        i, j = pile.pop()
        v = []
        if j < q - 1 and maze.valid_cells[i, j + 1] and not maze.grid[i][j + 1].visited:
            v.append('N')
        if i > 0 and maze.valid_cells[i - 1, j] and not maze.grid[i - 1][j].visited:
            v.append('W')
        if j > 0 and maze.valid_cells[i, j - 1] and not maze.grid[i][j - 1].visited:
            v.append('S')
        if i < p - 1 and maze.valid_cells[i + 1, j] and not maze.grid[i + 1][j].visited:
            v.append('E')
        if len(v) > 1:
            pile.push((i, j))
        if len(v) > 0:
            direction = v[randint(len(v))]

            if direction == 'N':
                maze.grid[i][j].N = True
                maze.grid[i][j + 1].S = True
                maze.grid[i][j + 1].visited = True
                pile.push((i, j + 1))
            elif direction == 'W':
                maze.grid[i][j].W = True
                maze.grid[i - 1][j].E = True
                maze.grid[i - 1][j].visited = True
                pile.push((i - 1, j))
            elif direction == 'S':
                maze.grid[i][j].S = True
                maze.grid[i][j - 1].N = True
                maze.grid[i][j - 1].visited = True
                pile.push((i, j - 1))
            else:
                maze.grid[i][j].E = True
                maze.grid[i + 1][j].W = True
                maze.grid[i + 1][j].visited = True
                pile.push((i + 1, j))
    return maze


def to_pdf(filename, level, n, shape, difficulty):
    rows = level["rows"]
    columns = level["columns"]
    if shape == "circle":
        new_dimension = max(rows, columns)
        rows = columns = new_dimension if new_dimension == 0 else new_dimension + 1
    """Generate and save `n` mazes of shapes `rows` x `columns` into a PDF file."""
    with PdfPages(filename) as pdf:
        for k in range(n):
            laby = creation(rows, columns, shape)
            plt.figure(figsize=(rows, columns))
            laby.canvas()

            plt.title(f"Maze level {difficulty}")

            # Supprimer les bordures et marges
            plt.gca().set_aspect('equal')
            plt.axis('off')  # Retire les axes
            plt.tight_layout(pad=0)  # Supprime les marges

            # Sauvegarder sans bordure
            pdf.savefig(bbox_inches='tight', pad_inches=0, facecolor='white')
            plt.close()


if __name__ == '__main__':
    # Shape of mazes
    levels = {1: {'rows': 10, 'columns': 5},
              2: {'rows': 15, 'columns': 10},
              3: {'rows': 20, 'columns': 15},
              4: {'rows': 25, 'columns': 20},
              5: {'rows': 30, 'columns': 20},
              6: {'rows': 40, 'columns': 30},
              7: {'rows': 50, 'columns': 35},
              8: {'rows': 60, 'columns': 45},
              9: {'rows': 70, 'columns': 55},
              10: {'rows': 90, 'columns': 60}
              }

    nbr_mazes = 4
    difficulty = 10
    forms = ["circle", "rectangular"]
    form = forms[1]

    level = levels[difficulty]

    to_pdf("mazes.pdf", level, nbr_mazes, form, difficulty)

    print(f"{nbr_mazes} mazes {form} of difficulty {difficulty} had be saved into file.")
