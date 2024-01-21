# Fling Solver
## Description

This is a solver for the game [Fling!](https://apps.apple.com/fr/app/fling/id325815008). It is written in Python 3.

## Usage

First, edit the file `puzzle.txt` to contain the puzzle you want to solve. The puzzle should be entered as a string of characters, with each row separated by a newline. The characters should be as follows:
- 0 for an empty space
- 1 for a ball

One row of the puzzle should be entered as a string of characters, with no spaces. For example, the puzzle

```
_ _ _ _ _ _ _
_ _ O _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ O _ _ _ O _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
``` 

would be entered as

```
0000000
0010000
0000000
0000000
0100010
0000000
0000000
```

You can miss out the trailing zeros, so the above puzzle could also be entered as

```

001


010001
```
(do not forget empty lines between rows for rows with no balls)

Then, run `python3 fling.py` in the terminal. The program will print the solution to the puzzle.

## Français

Ce programme résout les puzzles du jeu [Fling](https://play.google.com/store/apps/details?id=com.candycaneapps.flingsolve&hl=en_US&gl=US). Il est écrit en Python 3.

## Utilisation

Tout d'abord, éditez le fichier `puzzle.txt` pour qu'il contienne le puzzle que vous voulez résoudre. Le puzzle doit être entré comme une chaîne de caractères, chaque ligne étant séparée par un retour à la ligne. Les caractères doivent être les suivants :
- 0 pour un espace vide
- 1 pour une bille

Une ligne du puzzle doit être entrée comme une chaîne de caractères, sans espaces. Par exemple, le puzzle

```
_ _ _ _ _ _ _
_ _ O _ _ _ _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
_ O _ _ _ O _
_ _ _ _ _ _ _
_ _ _ _ _ _ _
```

serait entré ainsi :

```
0000000
0010000
0000000
0000000
0100010
0000000
0000000
```

Vous pouvez omettre les zéros de fin, donc le puzzle ci-dessus pourrait également être entré ainsi :

```

001


010001
```
(n'oubliez pas les lignes vides entre les lignes pour les lignes sans billes)

Ensuite, exécutez `python3 fling.py` dans le terminal. Le programme affichera la solution du puzzle.

# Algorithme

L'algorithme utilisé pour résoudre les puzzles s'appuie sur le parcours de graphes.

Dans un premier temps, on a créé une class `Board` qui représente un plateau de jeu. On a programmé
les règles du jeu dans cette class, ainsi que les méthodes permettant de déplacer les billes.

Pour un tableau donné, on a aussi une méthode permettant de trouver l'ensemble des déplacements possibles.

On a ensuite créé une classe "Graph" qui représente un graphe. Cette classe contient une liste de noeuds "GraphNode", chacun contenant une liste d'arêtes (sous forme de dictionnaire) permettant ainsi d'associer le mouvement de bille qui relie un plateau à un autre.

Chaque noeud représente un plateau de jeu (tableau dans un état donné), et chaque arête représente un déplacement de bille.

Lorsqu'on lance l'algorithme, on construit le graphe en commençant par l'état initial, puis en ajoutant les noeuds et les arêtes correspondant à tous les déplacements possibles. On s'arrête lorsque l'on a atteint l'état final, c'est-à-dire lorsqu'il ne reste plus qu'une seule bille sur le plateau.

Chaque noeud pour lequel on a calculé les déplacements possibles est marqué comme "visité". On ne calcule les déplacements possibles que pour les noeuds non visités. Cela permet d'éviter de calculer plusieurs fois les mêmes déplacements.

Une fois le graphe construit, on peut trouver le chemin le plus court entre l'état initial et l'état final. Pour cela, on utilise l'algorithme de parcours en largeur (BFS - Breadth First Search). Cet algorithme permet de trouver le chemin le plus court entre deux noeuds dans un graphe, ici un graphe orienté non pondéré.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- The game [Fling!](https://apps.apple.com/fr/app/fling/id325815008) was created by [Bevin Software OU](https://apps.apple.com/fr/developer/bevin-software-ou/id1053409328)

## Other projects

[A JavaScript Fling! Solver](http://littlefamily.us:8080/fling/solver.html)
