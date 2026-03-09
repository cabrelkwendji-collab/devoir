"""
maze.py - Génération et gestion du labyrinthe

Ce module fournit les fonctions nécessaires pour :
- Générer un labyrinthe 16x16 avec des murs aléatoires
- Garantir l'existence d'un chemin entre S et G
- Afficher le labyrinthe dans la console
- Obtenir les voisins valides d'une position
"""

import random
from collections import deque


def generate_maze(size=16, seed=None, wall_density=0.3):
    """
    Génère un labyrinthe de taille size x size.

    Args:
        size (int): Taille du labyrinthe (par défaut 16).
        seed (int ou None): Graine aléatoire pour la reproductibilité.
        wall_density (float): Proportion de murs intérieurs (0.0 à 1.0).

    Returns:
        list[list[str]]: Matrice 2D représentant le labyrinthe.
    """
    if seed is not None:
        random.seed(seed)

    # Initialiser la grille avec des cases libres
    maze = [['.' for _ in range(size)] for _ in range(size)]

    # Placer les bordures extérieures (murs)
    for i in range(size):
        for j in range(size):
            if i == 0 or i == size - 1 or j == 0 or j == size - 1:
                maze[i][j] = '#'

    # Définir le point de départ et le point d'arrivée
    start = (1, 1)
    goal = (size - 2, size - 2)
    maze[start[0]][start[1]] = 'S'
    maze[goal[0]][goal[1]] = 'G'

    # Placer des murs aléatoires à l'intérieur
    inner_cells = []
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if (i, j) != start and (i, j) != goal:
                inner_cells.append((i, j))

    # Mélanger et placer les murs selon la densité souhaitée
    random.shuffle(inner_cells)
    num_walls = int(len(inner_cells) * wall_density)

    for k in range(num_walls):
        r, c = inner_cells[k]
        maze[r][c] = '#'

    # Garantir qu'un chemin existe entre S et G
    _ensure_path_exists(maze, start, goal)

    return maze


def _ensure_path_exists(maze, start, goal):
    """
    Vérifie qu'un chemin existe entre start et goal.
    Si aucun chemin n'existe, retire des murs pour en créer un.

    Args:
        maze (list[list[str]]): Le labyrinthe à vérifier/modifier.
        start (tuple): Position de départ (row, col).
        goal (tuple): Position d'arrivée (row, col).
    """
    # Vérifier si un chemin existe avec un BFS rapide
    if _path_exists(maze, start, goal):
        return

    # Aucun chemin trouvé : on en crée un en retirant des murs
    # Utiliser un BFS depuis le départ pour trouver toutes les cases accessibles
    # Puis creuser un passage vers le but
    size = len(maze)

    # Trouver les cases accessibles depuis le départ
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        for neighbor in _get_adj(current, size):
            if neighbor not in visited:
                r, c = neighbor
                if maze[r][c] != '#':
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

    # Creuser un chemin direct du point accessible le plus proche du but vers le but
    # Trouver la case accessible la plus proche du but (distance de Manhattan)
    closest = min(visited, key=lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1]))

    # Creuser de closest vers goal
    current = closest
    while current != goal:
        r, c = current
        # Se rapprocher du but
        if r < goal[0]:
            r += 1
        elif r > goal[0]:
            r -= 1
        elif c < goal[1]:
            c += 1
        elif c > goal[1]:
            c -= 1

        next_cell = (r, c)
        if maze[r][c] == '#':
            maze[r][c] = '.'
        current = next_cell

    # Restaurer S et G au cas où ils auraient été écrasés
    maze[start[0]][start[1]] = 'S'
    maze[goal[0]][goal[1]] = 'G'


def _get_adj(pos, size):
    """
    Retourne les positions adjacentes (4 directions) dans les limites de la grille.

    Args:
        pos (tuple): Position courante (row, col).
        size (int): Taille du labyrinthe.

    Returns:
        list[tuple]: Liste des positions adjacentes valides.
    """
    r, c = pos
    adj = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size:
            adj.append((nr, nc))
    return adj


def _path_exists(maze, start, goal):
    """
    Vérifie l'existence d'un chemin entre start et goal via un BFS rapide.

    Args:
        maze (list[list[str]]): Le labyrinthe.
        start (tuple): Position de départ.
        goal (tuple): Position d'arrivée.

    Returns:
        bool: True si un chemin existe, False sinon.
    """
    size = len(maze)
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            return True
        for neighbor in _get_adj(current, size):
            if neighbor not in visited:
                r, c = neighbor
                if maze[r][c] != '#':
                    visited.add(neighbor)
                    queue.append(neighbor)

    return False


def get_neighbors(pos, maze):
    """
    Retourne les voisins accessibles d'une position dans le labyrinthe.
    Ordre : droite, bas, gauche, haut (cohérent pour tous les algorithmes).

    Args:
        pos (tuple): Position courante (row, col).
        maze (list[list[str]]): Le labyrinthe.

    Returns:
        list[tuple]: Liste des positions voisines accessibles.
    """
    r, c = pos
    size = len(maze)
    neighbors = []

    # Ordre : droite, bas, gauche, haut
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size and maze[nr][nc] != '#':
            neighbors.append((nr, nc))

    return neighbors


def print_maze(maze, title="Labyrinthe"):
    """
    Affiche le labyrinthe dans la console.

    Args:
        maze (list[list[str]]): Le labyrinthe à afficher.
        title (str): Titre à afficher au-dessus du labyrinthe.
    """
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print(f"{'=' * 40}")
    for row in maze:
        print(' '.join(row))
    print()


def print_maze_with_explored(maze, explored, title="Exploration"):
    """
    Affiche le labyrinthe avec les cases explorées marquées 'p'.

    Args:
        maze (list[list[str]]): Le labyrinthe original.
        explored (set): Ensemble des positions explorées.
        title (str): Titre de l'affichage.
    """
    # Créer une copie du labyrinthe
    display = [row[:] for row in maze]

    for r, c in explored:
        if display[r][c] == '.':
            display[r][c] = 'p'

    print_maze(display, title)


def print_maze_with_path(maze, path, title="Solution"):
    """
    Affiche le labyrinthe avec le chemin solution marqué '*'.

    Args:
        maze (list[list[str]]): Le labyrinthe original.
        path (list[tuple]): Liste ordonnée des positions du chemin.
        title (str): Titre de l'affichage.
    """
    # Créer une copie du labyrinthe
    display = [row[:] for row in maze]

    for r, c in path:
        if display[r][c] == '.':
            display[r][c] = '*'

    print_maze(display, title)


def print_path(path, start, goal):
    """
    Affiche le chemin sous forme de liste de coordonnées.

    Args:
        path (list[tuple]): Liste ordonnée des positions du chemin.
        start (tuple): Position de départ.
        goal (tuple): Position d'arrivée.
    """
    if not path:
        print("Aucun chemin trouvé.")
        return

    parts = []
    for i, (r, c) in enumerate(path):
        if (r, c) == start:
            parts.append(f"S({r}, {c})")
        elif (r, c) == goal:
            parts.append(f"G({r}, {c})")
        else:
            parts.append(f"({r}, {c})")

    print("Chemin: " + " -> ".join(parts))


def get_start_goal(maze):
    """
    Trouve les positions de S et G dans le labyrinthe.

    Args:
        maze (list[list[str]]): Le labyrinthe.

    Returns:
        tuple: (start, goal) avec start et goal en (row, col).
    """
    start = None
    goal = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'G':
                goal = (i, j)
    return start, goal


# --- Test rapide du module ---
if __name__ == "__main__":
    # Générer et afficher un labyrinthe avec une seed
    maze = generate_maze(size=16, seed=42, wall_density=0.3)
    print_maze(maze, "Labyrinthe 16x16 (seed=42)")

    # Vérifier les positions S et G
    start, goal = get_start_goal(maze)
    print(f"Départ : {start}")
    print(f"Arrivée : {goal}")

    # Vérifier qu'un chemin existe
    path_ok = _path_exists(maze, start, goal)
    print(f"Chemin existant : {path_ok}")

    # Afficher les voisins du départ
    neighbors = get_neighbors(start, maze)
    print(f"Voisins de {start} : {neighbors}")
