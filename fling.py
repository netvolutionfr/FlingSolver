import time

from Graphe import resolve
from Board import Board


if __name__ == '__main__':

    """ Résolution avec graphe """
    time_start = time.time()
    tab = Board()
    tab.load_from_file("puzzle.txt")
    print(f'Nombre de billes : {tab.count_balls()}')
    graph = resolve(tab)
    time_end = time.time()
    print("Temps d'exécution : " + str(time_end - time_start) + " secondes")