"""
main.py - Point d'entrée principal du projet
INF-5183 - Fondements de l'Intelligence Artificielle
"""

import sys
import time
from maze import (
    generate_maze, print_maze, copy_maze, get_start_goal, 
    WALL, START, GOAL, print_path
)
from dfs import dfs
from bfs import bfs
from astar import astar

def visualize_exploration(maze, explored, title="Exploration"):
    """Affiche la visualisation de l'exploration."""
    maze_viz = copy_maze(maze)
    for r, c in explored:
        if maze_viz[r][c] not in [START, GOAL, WALL]:
            maze_viz[r][c] = 'p'
    print_maze(maze_viz, title)

def visualize_solution(maze, path, title="Solution"):
    """Affiche la visualisation de la solution."""
    maze_viz = copy_maze(maze)
    for r, c in path:
        if maze_viz[r][c] not in [START, GOAL]:
            maze_viz[r][c] = '*'
    print_maze(maze_viz, title)

def print_comparison_table(results):
    """Affiche le tableau comparatif des performances."""
    print("\n" + "=" * 65)
    print(f"{'Algorithme':<20} | {'Nœuds':<10} | {'Longueur':<10} | {'Temps (ms)':<10}")
    print("-" * 65)
    for algo_name, res in results.items():
        print(f"{algo_name:<20} | {res['nodes_explored']:<10} | {res['path_length']:<10} | {res['exec_time']:<10.3f}")
    print("=" * 65)

def run_all_algorithms(maze, start, goal):
    """Exécute et compare les trois algorithmes."""
    results = {}
    algos = [
        ("DFS (Profondeur)", dfs),
        ("BFS (Largeur)", bfs),
        ("A* (Manhattan)", astar)
    ]

    for name, func in algos:
        print(f"\nExécution de {name}...")
        res = func(maze, start, goal)
        results[name] = res
        
        # Affichage visuel
        visualize_exploration(maze, res['explored'], f"{name} - Exploration (p)")
        visualize_solution(maze, res['path'], f"{name} - Solution (*)")
        
        # Affichage du chemin textuel
        print_path(res['path'], start, goal)

    return results

def main(seed=None):
    print("=" * 60)
    print("DEVOIR I - ALGORITHMES DE RECHERCHE DANS UN LABYRINTHE")
    print("=" * 60)
    
    if seed is None:
        import random
        seed = random.randint(0, 9999)
    
    print(f"\n[1] Génération du labyrinthe (Seed: {seed})...")
    maze = generate_maze(size=16, seed=seed)
    start, goal = get_start_goal(maze)
    
    print(f"Départ S: {start} | Arrivée G: {goal}")
    print_maze(maze, "Labyrinthe Initial")
    
    print("\n[2] Lancement des recherches...")
    results = run_all_algorithms(maze, start, goal)
    
    print("\n[3] Comparaison Finale")
    print_comparison_table(results)

if __name__ == "__main__":
    current_seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(current_seed)
