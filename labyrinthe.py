from numpy.random import randint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class Pile:
    def __init__(self):
        self.lst = []

    def empty(self):
        return self.lst == []

    def push(self, x):
        self.lst.append(x)

    def pop(self):
        if self.empty():
            raise ValueError("pile vide")
        return self.lst.pop()


class Case:
    def __init__(self):
        self.N = False
        self.W = False
        self.S = False
        self.E = False
        self.etat = False


def explorer(laby):
    pile = Pile()
    pile.push((0, laby.q - 1))
    laby.tab[0][laby.q - 1].etat = False
    while True:
        i, j = pile.pop()
        if i == laby.p - 1 and j == 0:
            break
        if j > 0 and laby.tab[i][j].S and laby.tab[i][j - 1].etat:
            pile.push((i, j))
            pile.push((i, j - 1))
            laby.tab[i][j - 1].etat = False
        elif i < laby.p - 1 and laby.tab[i][j].E and laby.tab[i + 1][j].etat:
            pile.push((i, j))
            pile.push((i + 1, j))
            laby.tab[i + 1][j].etat = False
        elif j < laby.q - 1 and laby.tab[i][j].N and laby.tab[i][j + 1].etat:
            pile.push((i, j))
            pile.push((i, j + 1))
            laby.tab[i][j + 1].etat = False
        elif i > 0 and laby.tab[i][j].W and laby.tab[i - 1][j].etat:
            pile.push((i, j))
            pile.push((i - 1, j))
            laby.tab[i - 1][j].etat = False
    return pile.lst


class Labyrinthe:
    def __init__(self, p, q, forme="rectangle"):
        self.p = p
        self.q = q
        self.tab = [[Case() for j in range(q)] for i in range(p)]
        self.forme = forme
        self.valid_cells = self._generate_valid_cells()

    def _generate_valid_cells(self):
        """Génère une matrice indiquant si chaque cellule est valide en fonction de la forme."""
        valid = np.ones((self.p, self.q), dtype=bool)
        if self.forme == "cercle":
            cx, cy = self.p // 2, self.q // 2
            rayon = min(self.p, self.q) // 2
            for i in range(self.p):
                for j in range(self.q):
                    if (i - cx) ** 2 + (j - cy) ** 2 > rayon ** 2:
                        valid[i, j] = False
        return valid

    def canvas(self):
        line_start = randint((self.q) / 2) + round(self.q / 2)
        line_arrive = randint(self.q / 2)
        lw = 4

        # interior borders
        for i in range(self.p - 1):
            for j in range(self.q):
                if not self.tab[i][j].E and self.valid_cells[i, j] and self.valid_cells[i + 1, j]:
                    plt.plot([i + 1, i + 1], [j, j + 1], 'b', linewidth=lw)
        for j in range(self.q - 1):
            for i in range(self.p):
                if not self.tab[i][j].N and self.valid_cells[i, j] and self.valid_cells[i, j + 1]:
                    plt.plot([i, i + 1], [j + 1, j + 1], 'b', linewidth=lw)

        # Parcours chaque cellule
        for i in range(self.p):
            for j in range(self.q):
                if not self.valid_cells[i, j]:
                    continue  # Ignore les cellules non valides

                # Vérifie les bordures et dessine les murs manquants
                # Ouest (gauche)
                if i == 0 or not self.valid_cells[i - 1, j]:
                    if j == line_start:
                        plt.plot(i - 0.5, j + 0.5, marker='o', color='green', markersize=9, label='Départ', solid_capstyle="round")
                    else:
                        plt.plot([i, i], [j, j + 1], 'b', linewidth=lw+1, solid_capstyle="round")  # Mur gauche

                # Est (droite)
                if i == self.p - 1 or not self.valid_cells[i + 1, j]:
                    if j == line_arrive:
                        plt.plot(i + 1.5, j + 0.5, marker='*', color='red', markersize=9, label='Arrivée', solid_capstyle="round")
                    else:
                        plt.plot([i + 1, i + 1], [j, j + 1], 'b', linewidth=lw+1, solid_capstyle="round")  # Mur droit

                # Sud (bas)
                if j == 0 or not self.valid_cells[i, j - 1]:
                    plt.plot([i, i + 1], [j, j], 'b', linewidth=lw+1, solid_capstyle="round")  # Mur bas

                # Nord (haut)
                if j == self.q - 1 or not self.valid_cells[i, j + 1]:
                    plt.plot([i, i + 1], [j + 1, j + 1], 'b', linewidth=lw+1, solid_capstyle="round")  # Mur haut

        plt.axis('off')

    def solution(self):
        sol = explorer(self)
        X, Y = [], []
        for (i, j) in sol:
            X.append(i + .5)
            Y.append(j + .5)
        X.append(self.p - .5)
        Y.append(.5)
        plt.plot(X, Y, 'r', linewidth=2)

    def show(self):
        self.canvas()
        plt.show()


def creation(p, q, forme="rectangle"):
    laby = Labyrinthe(p, q, forme)
    pile = Pile()
    while True:
        i, j = randint(p), randint(q)
        if laby.valid_cells[i, j]:
            break
    pile.push((i, j))
    laby.tab[i][j].etat = True
    while not pile.empty():
        i, j = pile.pop()
        v = []
        if j < q - 1 and laby.valid_cells[i, j + 1] and not laby.tab[i][j + 1].etat:
            v.append('N')
        if i > 0 and laby.valid_cells[i - 1, j] and not laby.tab[i - 1][j].etat:
            v.append('W')
        if j > 0 and laby.valid_cells[i, j - 1] and not laby.tab[i][j - 1].etat:
            v.append('S')
        if i < p - 1 and laby.valid_cells[i + 1, j] and not laby.tab[i + 1][j].etat:
            v.append('E')
        if len(v) > 1:
            pile.push((i, j))
        if len(v) > 0:
            c = v[randint(len(v))]
            if c == 'N':
                laby.tab[i][j].N = True
                laby.tab[i][j + 1].S = True
                laby.tab[i][j + 1].etat = True
                pile.push((i, j + 1))
            elif c == 'W':
                laby.tab[i][j].W = True
                laby.tab[i - 1][j].E = True
                laby.tab[i - 1][j].etat = True
                pile.push((i - 1, j))
            elif c == 'S':
                laby.tab[i][j].S = True
                laby.tab[i][j - 1].N = True
                laby.tab[i][j - 1].etat = True
                pile.push((i, j - 1))
            else:
                laby.tab[i][j].E = True
                laby.tab[i + 1][j].W = True
                laby.tab[i + 1][j].etat = True
                pile.push((i + 1, j))
    return laby


def to_pdf(filename, niveau, n, forme, difficulte):
    p = niveau["lignes"]
    q = niveau["colonnes"]
    """Génère et sauvegarde `n` labyrinthes de dimensions `p` x `q` dans un fichier PDF."""
    with PdfPages(filename) as pdf:
        for k in range(n):
            laby = creation(p, q, forme)
            plt.figure(figsize=(8, 8))
            laby.canvas()
            plt.title(f"Labyrinthe niveau {difficulte}")
            pdf.savefig()  # Sauvegarde la figure dans le PDF
            plt.close()  # Ferme la figure pour libérer la mémoire


if __name__ == '__main__':
    # Dimensions des labyrinthes
    niveaux = {1: {'lignes': 10, 'colonnes': 5},
               2: {'lignes': 15, 'colonnes': 10},
               3: {'lignes': 20, 'colonnes': 15},
               4: {'lignes': 25, 'colonnes': 20},
               5: {'lignes': 30, 'colonnes': 20},
               6: {'lignes': 40, 'colonnes': 30},
               9: {'lignes': 60, 'colonnes': 55}
               }

    nombre_labyrinthes = 24
    difficulte = 3
    forme = "rectangle"
    forme = "cercle"

    niveau = niveaux[difficulte]

    # Génération et sauvegarde des labyrinthes dans un PDF
    to_pdf("labyrinthes.pdf", niveau, nombre_labyrinthes, forme, difficulte)

    print(f"{nombre_labyrinthes} labyrinthes de difficulté {difficulte} en forme de {forme} ont été enregistrés dans le fichier.")
