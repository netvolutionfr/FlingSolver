from collections import deque
from Board import Board


class GraphNode:
    """ Représentation d'un nœud dans le graphe """
    def __init__(self, board):
        self.board = board
        self.board_id = board.get_id()
        self.edges = {}  # Dictionnaire pour les arcs: clé = tableau cible, valeur = mouvement
        self.expanded = False


class Graph:
    """ Représentation du graphe """
    def __init__(self):
        self.nodes = {}  # Dictionnaire pour les nœuds: clé = id du tableau, valeur = objet GraphNode

    def add_node(self, board):
        """ Ajoute un nœud au graphe """
        node = GraphNode(board)
        self.nodes[node.board_id] = node
        return node

    def add_edge(self, from_board, to_board, move):
        """ Ajoute un arc au graphe """
        if from_board.get_id() not in self.nodes:
            self.add_node(from_board)
        if to_board.get_id() not in self.nodes:
            self.add_node(to_board)

        self.nodes[from_board.get_id()].edges[to_board.get_id()] = move

    def expand(self, node):
        """ Création des arcs sortants """
        if node.expanded:
            return
        node.expanded = True
        for move in node.board.possible_moves():
            tab = node.board.copy()
            tab.move(move[0], move[1], move[2])
            self.add_edge(node.board, tab, move)

            if tab.count_balls() == 1:
                raise SolutionFoundException(f"Solution trouvée", tab.get_id())
            self.expand(self.nodes[tab.get_id()])


class SolutionFoundException(Exception):
    def __init__(self, message, solution_id):
        super().__init__(message)
        self.solution_id = solution_id


def resolve(board):
    """ Résolution du jeu Fling """
    graph = Graph()
    initial_node = graph.add_node(board)
    try:
        # Supposons que `initial_node` est votre nœud de départ
        graph.expand(initial_node)
    except SolutionFoundException as e:
        solution_id = e.solution_id
        # Utilisation de la fonction
        start_node_id = board.get_id()  # L'ID du nœud de départ
        end_node_id = solution_id  # L'ID du nœud d'arrivée
        path = find_path(graph, start_node_id, end_node_id)

        if path:
            print("Longueur du chemin : " + str(len(path) - 1))
            print("Taille du graphe : " + str(len(graph.nodes)))
            for i in range(len(path) - 1):
                node_id = path[i]
                next_node_id = path[i + 1]
                tab = Board()
                tab.set_id(node_id)
                # print(tab)
                move = graph.nodes[node_id].edges[next_node_id]
                print(move)
        else:
            print("Aucun chemin trouvé.")
    return graph


def find_path(graph, start_id, end_id):
    visited = set()
    queue = deque([(start_id, [])])  # La queue contient des paires (node_id, path)

    while queue:
        current_id, path = queue.popleft()
        if current_id in visited:
            continue

        visited.add(current_id)
        path = path + [current_id]

        if current_id == end_id:
            return path

        for next_id in graph.nodes[current_id].edges:
            if next_id not in visited:
                queue.append((next_id, path))

    return None  # Si aucun chemin n'est trouvé



