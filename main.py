"""
main.py - Point d'entrée principal du programme

Ce fichier :
1. Génère un labyrinthe 16x16
2. Exécute les 3 algorithmes (DFS, BFS, A*)
3. Affiche les résultats pour chaque algorithme
4. Affiche un tableau comparatif final
"""

from maze import (
    generate_maze,
    get_start_goal,
    print_maze,
    print_maze_with_explored,
    print_maze_with_path,
    print_path
)
from dfs import dfs
from bfs import bfs
from astar import astar


def print_separator():
    """Affiche une ligne de séparation."""
    print("\n" + "=" * 60)


def print_results(name, maze, results, start, goal):
    """
    Affiche tous les résultats d'un algorithme.

    Args:
        name (str): Nom de l'algorithme.
        maze (list[list[str]]): Le labyrinthe.
        results (dict): Résultats de l'algorithme.
        start (tuple): Position de départ.
        goal (tuple): Position d'arrivée.
    """
    print_separator()
    print(f"  ALGORITHME : {name}")
    print_separator()

    # Afficher l'exploration
    print_maze_with_explored(maze, results['explored'], f"{name} - Exploration")

    # Afficher la solution
    print_maze_with_path(maze, results['path'], f"{name} - Solution")

    # Afficher le chemin
    print_path(results['path'], start, goal)

    # Afficher les statistiques
    print(f"\n--- Statistiques {name} ---")
    print(f"Noeuds explorés  : {results['nodes_explored']}")
    print(f"Longueur chemin  : {results['path_length']}")
    print(f"Temps exécution  : {results['exec_time']:.3f} ms")


def print_comparison_table(dfs_results, bfs_results, astar_results):
    """
    Affiche le tableau comparatif des 3 algorithmes.

    Args:
        dfs_results (dict): Résultats du DFS.
        bfs_results (dict): Résultats du BFS.
        astar_results (dict): Résultats du A*.
    """
    print_separator()
    print("  TABLEAU COMPARATIF")
    print_separator()

    # En-tête du tableau
    print(f"\n{'Algorithme':<20} {'Noeuds':<12} {'Longueur':<12} {'Temps (ms)':<12}")
    print("-" * 56)

    # Ligne DFS
    print(f"{'DFS':<20} {dfs_results['nodes_explored']:<12} "
          f"{dfs_results['path_length']:<12} "
          f"{dfs_results['exec_time']:<12.3f}")

    # Ligne BFS
    print(f"{'BFS':<20} {bfs_results['nodes_explored']:<12} "
          f"{bfs_results['path_length']:<12} "
          f"{bfs_results['exec_time']:<12.3f}")

    # Ligne A*
    print(f"{'A* (manhattan)':<20} {astar_results['nodes_explored']:<12} "
          f"{astar_results['path_length']:<12} "
          f"{astar_results['exec_time']:<12.3f}")

    print()


def main():
    """
    Fonction principale du programme.
    Génère le labyrinthe, exécute les 3 algorithmes et affiche les résultats.
    """
    # ============================================
    # 1. GÉNÉRATION DU LABYRINTHE
    # ============================================
    print_separator()
    print("  GÉNÉRATION DU LABYRINTHE")
    print_separator()

    # Tu peux changer la seed pour obtenir un labyrinthe différent
    # Exemples : seed=42, seed=123, seed=2026
    SEED = 42
    SIZE = 16
    WALL_DENSITY = 0.3

    print(f"\nParamètres :")
    print(f"  Taille       : {SIZE}x{SIZE}")
    print(f"  Seed         : {SEED}")
    print(f"  Densité murs : {WALL_DENSITY}")

    maze = generate_maze(size=SIZE, seed=SEED, wall_density=WALL_DENSITY)
    start, goal = get_start_goal(maze)

    print(f"  Départ       : {start}")
    print(f"  Arrivée      : {goal}")

    # Afficher le labyrinthe original
    print_maze(maze, "Labyrinthe original")

    # ============================================
    # 2. EXÉCUTION DES ALGORITHMES
    # ============================================

    # --- DFS ---
    dfs_results = dfs(maze, start, goal)
    print_results("DFS", maze, dfs_results, start, goal)

    # --- BFS ---
    bfs_results = bfs(maze, start, goal)
    print_results("BFS", maze, bfs_results, start, goal)

    # --- A* ---
    astar_results = astar(maze, start, goal)
    print_results("A* (Manhattan)", maze, astar_results, start, goal)

    # ============================================
    # 3. TABLEAU COMPARATIF
    # ============================================
    print_comparison_table(dfs_results, bfs_results, astar_results)

    # ============================================
    # 4. OBSERVATIONS
    # ============================================
    print_separator()
    print("  OBSERVATIONS")
    print_separator()

    # Comparer les longueurs des chemins
    print(f"\n• DFS a trouvé un chemin de longueur {dfs_results['path_length']}")
    print(f"• BFS a trouvé un chemin de longueur {bfs_results['path_length']}")
    print(f"• A*  a trouvé un chemin de longueur {astar_results['path_length']}")

    if bfs_results['path_length'] == astar_results['path_length']:
        print("\n✅ BFS et A* trouvent le même chemin optimal.")

    if dfs_results['path_length'] > bfs_results['path_length']:
        print("⚠️  DFS trouve un chemin plus long (non optimal).")
    elif dfs_results['path_length'] == bfs_results['path_length']:
        print("✅ DFS a aussi trouvé un chemin optimal dans ce cas.")

    # Comparer les noeuds explorés
    print(f"\n• DFS a exploré {dfs_results['nodes_explored']} noeuds")
    print(f"• BFS a exploré {bfs_results['nodes_explored']} noeuds")
    print(f"• A*  a exploré {astar_results['nodes_explored']} noeuds")

    if astar_results['nodes_explored'] <= bfs_results['nodes_explored']:
        print("\n✅ A* explore moins ou autant de noeuds que BFS grâce à l'heuristique.")

    print()


# --- Lancer le programme ---
if __name__ == "__main__":
    main()
