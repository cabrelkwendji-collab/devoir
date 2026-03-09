"""
dfs.py - Implémentation de l'algorithme DFS (Depth-First Search)

Recherche en profondeur utilisant une pile (LIFO).
Explore les voisins dans l'ordre : droite, bas, gauche, haut.
"""

import time
from maze import get_neighbors


def dfs(maze, start, goal):
    """
    Exécute l'algorithme DFS pour trouver un chemin de start à goal.

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
    # Démarrer le chronomètre
    start_time = time.perf_counter()

    # Initialiser la pile (LIFO)
    stack = [start]

    # Ensemble des noeuds déjà visités
    visited = set()

    # Dictionnaire pour reconstruire le chemin : enfant -> parent
    parent = {start: None}

    # Ensemble de tous les noeuds explorés (pour la visualisation)
    explored = set()

    # Variable pour savoir si on a trouvé le but
    found = False

    # --- Boucle principale du DFS ---
    while stack:
        # Dépiler le dernier élément (LIFO)
        current = stack.pop()

        # Si ce noeud a déjà été visité, on l'ignore
        if current in visited:
            continue

        # Marquer comme visité
        visited.add(current)
        explored.add(current)

        # Vérifier si on a atteint le but
        if current == goal:
            found = True
            break

        # Obtenir les voisins (droite, bas, gauche, haut)
        neighbors = get_neighbors(current, maze)

        # IMPORTANT : on inverse l'ordre des voisins avant de les empiler
        # Car la pile (LIFO) va dépiler le dernier ajouté en premier
        # On veut explorer dans l'ordre : droite, bas, gauche, haut
        # Donc on empile dans l'ordre inverse : haut, gauche, bas, droite
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)
                # Enregistrer le parent seulement si pas encore connu
                if neighbor not in parent:
                    parent[neighbor] = current

    # Arrêter le chronomètre
    end_time = time.perf_counter()
    exec_time = (end_time - start_time) * 1000  # Convertir en millisecondes

    # --- Reconstruire le chemin ---
    path = []
    if found:
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()  # Inverser pour avoir start -> goal

    # --- Préparer les résultats ---
    results = {
        'explored': explored,
        'path': path,
        'nodes_explored': len(explored),
        'path_length': len(path),
        'exec_time': exec_time
    }

    return results


# --- Test rapide du module ---
if __name__ == "__main__":
    from maze import generate_maze, get_start_goal
    from maze import print_maze, print_maze_with_explored, print_maze_with_path, print_path

    # Générer un labyrinthe
    maze = generate_maze(size=16, seed=42, wall_density=0.3)
    start, goal = get_start_goal(maze)

    # Afficher le labyrinthe original
    print_maze(maze, "Labyrinthe original")

    # Exécuter DFS
    results = dfs(maze, start, goal)

    # Afficher l'exploration
    print_maze_with_explored(maze, results['explored'], "DFS - Exploration")

    # Afficher la solution
    print_maze_with_path(maze, results['path'], "DFS - Solution")

    # Afficher le chemin
    print_path(results['path'], start, goal)

    # Afficher les statistiques
    print(f"\n--- Statistiques DFS ---")
    print(f"Noeuds explorés : {results['nodes_explored']}")
    print(f"Longueur du chemin : {results['path_length']}")
    print(f"Temps d'exécution : {results['exec_time']:.3f} ms")