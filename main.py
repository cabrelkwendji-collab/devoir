"""
main.py - Point d'entrée principal du projet

Usage: python main.py [seed]

"""

import sys
from maze import generate_maze, print_maze, copy_maze, get_start_goal, WALL, START, GOAL
from dfs import dfs, format_path as dfs_format_path
from bfs import bfs, format_path as bfs_format_path
from astar import astar, format_path as astar_format_path


def visualize_exploration(maze, explored, title="Exploration"):
    """Affiche la visualisation de l'exploration."""
    maze_viz = copy_maze(maze)
    for pos in explored:
        if maze_viz[pos[0]][pos[1]] not in [START, GOAL, WALL]:
            maze_viz[pos[0]][pos[1]] = 'p'
    print_maze(maze_viz, title)


def visualize_solution(maze, path, title="Solution"):
    """Affiche la visualisation de la solution."""
    maze_viz = copy_maze(maze)
    for pos in path:
        if maze_viz[pos[0]][pos[1]] not in [START, GOAL]:
            maze_viz[pos[0]][pos[1]] = '*'
    print_maze(maze_viz, title)


def print_comparison_table(results):
    """Affiche le tableau comparatif."""
    print("\n" + "=" * 60)
    print("TABLEAU COMPARATIF")
    print("=" * 60)
    print(f"{'Algorithme':<20} {'Noeuds':<12} {'Longueur':<12} {'Temps (ms)':<12}")
    print("-" * 60)
    
    for algo_name, result in results.items():
        nodes = result['nodes_explored']
        length = result['path_length']
        time_ms = result['exec_time'] * 1000
        print(f"{algo_name:<20} {nodes:<12} {length:<12} {time_ms:<12.3f}")
    
    print("=" * 60)


def run_all_algorithms(maze, start, goal):
    """Exécute les trois algorithmes."""
    results = {}
    
    # DFS
    print("\n" + "=" * 60)
    print("ALGORITHME DFS (Depth-First Search)")
    print("=" * 60)
    result_dfs = dfs(maze, start, goal)
    results['DFS'] = result_dfs
    
    if result_dfs['found']:
        visualize_exploration(maze, result_dfs['explored'], "Exploration DFS (p = parcouru)")
        visualize_solution(maze, result_dfs['path'], "Solution DFS (* = chemin)")
        print(dfs_format_path(result_dfs['path'], start, goal))
        print(f"\nStatistiques DFS:")
        print(f"  - Nœuds explorés: {result_dfs['nodes_explored']}")
        print(f"  - Longueur du chemin: {result_dfs['path_length']}")
        print(f"  - Temps d'exécution: {result_dfs['exec_time']*1000:.3f} ms")
    else:
        print("Aucun chemin trouvé par DFS!")
    
    # BFS
    print("\n" + "=" * 60)
    print("ALGORITHME BFS (Breadth-First Search)")
    print("=" * 60)
    result_bfs = bfs(maze, start, goal)
    results['BFS'] = result_bfs
    
    if result_bfs['found']:
        visualize_exploration(maze, result_bfs['explored'], "Exploration BFS (p = parcouru)")
        visualize_solution(maze, result_bfs['path'], "Solution BFS (* = chemin)")
        print(bfs_format_path(result_bfs['path'], start, goal))
        print(f"\nStatistiques BFS:")
        print(f"  - Nœuds explorés: {result_bfs['nodes_explored']}")
        print(f"  - Longueur du chemin: {result_bfs['path_length']} (optimal)")
        print(f"  - Temps d'exécution: {result_bfs['exec_time']*1000:.3f} ms")
    else:
        print("Aucun chemin trouvé par BFS!")
    
    # A*
    print("\n" + "=" * 60)
    print("ALGORITHME A* (A-Star avec heuristique Manhattan)")
    print("=" * 60)
    result_astar = astar(maze, start, goal)
    results['A* (manhattan)'] = result_astar
    
    if result_astar['found']:
        visualize_exploration(maze, result_astar['explored'], "Exploration A* (p = parcouru)")
        visualize_solution(maze, result_astar['path'], "Solution A* (* = chemin)")
        print(astar_format_path(result_astar['path'], start, goal))
        print(f"\nStatistiques A*:")
        print(f"  - Nœuds explorés: {result_astar['nodes_explored']}")
        print(f"  - Longueur du chemin: {result_astar['path_length']} (optimal)")
        print(f"  - Temps d'exécution: {result_astar['exec_time']*1000:.3f} ms")
    else:
        print("Aucun chemin trouvé par A*!")
    
    return results


def main(seed=None):
    """Fonction principale."""
    print("=" * 60)
    print("DEVOIR I - ALGORITHMES DE RECHERCHE DANS UN LABYRINTHE")
    print("INF-5183 - Fondements de l'Intelligence Artificielle")
    print("=" * 60)
    
    if seed is not None:
        print(f"\nSeed utilisée: {seed}")
    else:
        import random
        seed = random.randint(0, 999999)
        print(f"\nSeed générée aléatoirement: {seed}")
    
    print("\n[1] Génération du labyrinthe 16x16...")
    maze = generate_maze(size=16, seed=seed)
    start, goal = find_start_goal(maze)
    
    print(f"    Point de départ S: {start}")
    print(f"    Point d'arrivée G: {goal}")
    print_maze(maze, "Labyrinthe généré")
    
    print("\n[2] Exécution des algorithmes de recherche...")
    results = run_all_algorithms(maze, start, goal)
    
    print("\n[3] Comparaison des résultats")
    print_comparison_table(results)
    
    print("\n" + "=" * 60)
    print("FIN DE L'EXÉCUTION")
    print("=" * 60)


if __name__ == "__main__":
    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print(f"Erreur: '{sys.argv[1]}' n'est pas un entier valide")
            sys.exit(1)
    
    main(seed)
