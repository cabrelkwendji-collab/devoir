"""
bfs.py - Implémentation de l'algorithme BFS (Breadth-First Search)

Recherche en largeur utilisant une file (FIFO).
Explore les voisins dans l'ordre : droite, bas, gauche, haut.
BFS garantit le chemin le plus court dans un labyrinthe non pondéré.
"""

import time
from collections import deque
from maze import get_neighbors


def bfs(maze, start, goal):
    """
    Exécute l'algorithme BFS pour trouver un chemin de start à goal.

    Args:
        maze (list[list[str]]): Le labyrinthe.
        start (tuple): Position de départ (row, col).
        goal (tuple): Position d'arrivée (row, col).

    Returns:
        dict: Dictionnaire contenant :
            - 'explored' (set): Ensemble des cases visitées
            - 'path' (list): Liste ordonnée des positions du chemin
            - 'nodes_explored' (int): Nombre de noeuds explorés
            - 'path_length' (int): Longueur du chemin trouvé
            - 'exec_time' (float): Temps d'exécution en millisecondes
    """
    start_time = time.perf_counter()

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    explored = set()
    found = False

    while queue:
        current = queue.popleft()
        explored.add(current)

        if current == goal:
            found = True
            break

        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current

    end_time = time.perf_counter()
    exec_time = (end_time - start_time) * 1000

    path = []
    if found:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()

    results = {
        'explored': explored,
        'path': path,
        'nodes_explored': len(explored),
        'path_length': len(path),
        'exec_time': exec_time
    }

    return results


if __name__ == "__main__":
    from maze import generate_maze, get_start_goal
    from maze import print_maze, print_maze_with_explored, print_maze_with_path, print_path

    maze = generate_maze(size=16, seed=42, wall_density=0.3)
    start, goal = get_start_goal(maze)

    print_maze(maze, "Labyrinthe original")

    results = bfs(maze, start, goal)

    print_maze_with_explored(maze, results['explored'], "BFS - Exploration")
    print_maze_with_path(maze, results['path'], "BFS - Solution")
    print_path(results['path'], start, goal)

    print(f"\n--- Statistiques BFS ---")
    print(f"Noeuds explorés : {results['nodes_explored']}")
    print(f"Longueur du chemin : {results['path_length']}")
    print(f"Temps d'exécution : {results['exec_time']:.3f} ms")
