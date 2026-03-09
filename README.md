## Devoir I — Algorithmes de Recherche dans un Labyrinthe

## 1) Informations du cours 

Cours : INF-5183
Université : UQO
Enseignant : Mohamed Lamine ALLAOUI


## 2) Objectif

Ce projet implémente trois algorithmes de recherche pour résoudre un labyrinthe 16x16 :

- **DFS** (Depth-First Search) — Recherche en profondeur
- **BFS** (Breadth-First Search) — Recherche en largeur
- **A\*** (A-Star) — Recherche informée avec heuristique de Manhattan

## 3) Structure du Projet

Devoir-1-IA/
maze.py # Génération et gestion du labyrinthe
dfs.py # Implémentation de DFS
bfs.py # Implémentation de BFS
astar.py # Implémentation de A*
main.py # Point d'entrée principal
requirements.txt # Dépendances (bibliothèque standard uniquement)
README.md # Ce fichier

## 4)  Prérequis

- Python 3.11 ou supérieur
- Aucune dépendance externe requise (bibliothèque standard uniquement)

## 5) Installation et Exécution

  ### 1. Cloner le dépôt

```bash
  git clone https://github.com/cabrelkwendji-collab/Kwendji_rep/DevoirI.git
  cd Devoir-1-IA

  ### 2. Exécuter le programme

python main.py

## 6) Résultats
Le programme affiche pour chaque algorithme :

Exploration : Visualisation des cases parcourues (marquées p)
Solution : Visualisation du chemin trouvé (marqué *)
Chemin : Liste des coordonnées du chemin
Statistiques : Noeuds explorés, longueur du chemin, temps d'exécution
Un tableau comparatif résume les performances des trois algorithmes.

Exemple de sortie
text

Algorithme           Noeuds       Longueur     Temps (ms)
--------------------------------------------------------
DFS                  78           45           0.521
BFS                  112          27           0.634
A* (manhattan)       45           27           0.312

## 7) Description des Algorithmes

DFS (Depth-First Search)
 Utilise une pile (LIFO)
 Explore en profondeur avant de revenir en arrière
 Ne garantit pas le chemin le plus court

BFS (Breadth-First Search)
 Utilise une file (FIFO)
 Explore couche par couche
 Garantit le chemin le plus court

A* (A-Star)
 Utilise une file de priorité
 Fonction d'évaluation : f(n) = g(n) + h(n)
   g(n) : coût réel depuis le départ
   h(n) : distance de Manhattan jusqu'au but
 Garantit le chemin le plus court
 Plus efficace que BFS grâce à l'heuristique

## 8) Paramètres Modifiables

 Dans main.py, vous pouvez modifier :

Python

  SEED = 42            # Graine aléatoire (changer pour un autre labyrinthe)
  SIZE = 16            # Taille du labyrinthe
  WALL_DENSITY = 0.3   # Densité des murs (0.0 = vide, 1.0 = plein)

## 9) Représentation du Labyrinthe

Symbole	Signification
 #	Mur (obstacle)
 .	Case libre
 S	Point de départ
 G	Point d'arrivée
 p	Case explorée
 *	Chemin 