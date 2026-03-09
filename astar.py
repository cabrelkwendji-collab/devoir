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

    # --- Initialisation 