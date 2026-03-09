"""
astar.py - Implémentation de l'algorithme A* (A-Star)

Recherche informée utilisant une file de priorité.
Fonction d'évaluation : f(n) = g(n) + h(n)
    - g(n) : coût réel du chemin depuis le départ jusqu'au noeud n
    - h(n) : estimation heuristique (distance de Manhattan)
Heuristique : h(n) = |x_n - x_G| + |y_n - y_G|
"""

import time
import heapq
from maze import get_neighbors


def manhattan_distance(pos, goal):
    """
    Calcule la distance de Manhattan entre deux positions.

    C'est comme compter le nombre de rues à parcourir
    dans une ville en grille (pas en diagonale).

    Args:
        pos (tuple): Position courante (row, col).
        goal (tuple): Position d'arrivée (row, col).

    Returns:
        int: Distance de Manhattan.
    """
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar(maze, start, goal):
    """
    Exécute l'algorithme A* pour trouver un chemin de start à goal.

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

    # --- Initialisation ---

    # File de priorité : (f_score, compteur, position)
    # Le compteur sert à départager les noeuds qui ont le même f_score
    # Sans le compteur, Python ne saurait pas comment comparer deux tuples
    counter = 0
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start, goal), counter, start))

    # g_score : coût réel du chemin depuis le départ
    # Au début, seul le départ a un coût de 0
    g_score = {start: 0}

    # f_score : estimation du coût total (g + h)
    f_score = {start: manhattan_distance(start, goal)}

    # Dictionnaire pour reconstruire le chemin : enfant -> parent
    parent = {start: None}

    # Ensemble des noeuds déjà traités (fermés)
    closed_set = set()

    # Ensemble des noeuds explorés (pour la visualisation)
    explored = set()

    # Variable pour savoir si on a trouvé le but
    found = False

    # --- Boucle principale de A* ---
    while open_list:
        # Retirer le noeud avec le plus petit f_score
        current_f, _, current = heapq.heappop(open_list)

        # Si ce noeud a déjà été traité, on l'ignore
        if current in closed_set:
            continue

        # Marquer comme traité
        closed_set.add(current)
        explored.add(current)

        # Vérifier si on a atteint le but
        if current == goal:
            found = True
            break

        # Obtenir les voisins (droite, bas, gauche, haut)
        neighbors = get_neighbors(current, maze)

        for neighbor in neighbors:
            # Ignorer les noeuds déjà traités
            if neighbor in closed_set:
                continue

            # Calculer le nouveau g_score pour ce voisin
            # Chaque déplacement coûte 1
            tentative_g = g_score[current] + 1

            # Si on a trouvé un meilleur chemin vers ce voisin
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                # Mettre à jour les scores
                g_score[neighbor] = tentative_g
                h = manhattan_distance(neighbor, goal)
                f = tentative_g + h
                f_score[neighbor] = f

                # Enregistrer le parent
                parent[neighbor] = current

                # Ajouter dans la file de priorité
                counter += 1
                heapq.heappush(open_list, (f, counter, neighbor))

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

    # Exécuter A*
    results = astar(maze, start, goal)

    # Afficher l'exploration
    print_maze_with_explored(maze, results['explored'], "A* - Exploration")

    # Afficher la solution
    print_maze_with_path(maze, results['path'], "A* - Solution")

    # Afficher le chemin
    print_path(results['path'], start, goal)

    # Afficher les statistiques
    print(f"\n--- Statistiques A* (Manhattan) ---")
    print(f"Noeuds explorés : {results['nodes_explored']}")
    print(f"Longueur du chemin : {results['path_length']}")
    print(f"Temps d'exécution : {results['exec_time']:.3f} ms")
