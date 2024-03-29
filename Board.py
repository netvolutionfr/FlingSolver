class Board():
    """ Représentation du tableau du jeu Fling """
    def __init__(self, lines = 8, columns = 7):
        """ Constructeur de la classe Tableau """
        self.lines = lines
        self.columns = columns
        self.board = [[0 for i in range(columns)] for j in range(lines)]

    def __str__(self):
        """ Affichage du tableau """
        my_string = ""
        for i in range(self.lines):
            for j in range(self.columns):
                if self.board[i][j] == 0:
                    my_string += ". "
                else:
                    my_string += "O "
            my_string += "\n"
        return my_string

    def get_id(self):
        """ Retourne l'identifiant du tableau """
        """ C'est un nombre binaire formé par la concaténation des lignes """
        """ du tableau """
        id = 0
        for i in range(self.lines):
            for j in range(self.columns):
                id = id << 1
                id += self.board[i][j]
        return id

    def set_id(self, id):
        """ Initialise le tableau à partir de son identifiant """
        """ On transforme le nombre en binaire et on place les 1 comme billes dans le tableau """
        id_tmp = id
        for i in range(self.lines - 1, -1, -1):
            for j in range(self.columns - 1, -1, -1):
                self.board[i][j] = id_tmp % 2
                id_tmp = id_tmp >> 1

    def all_ball(self, x, y):
        """ Ajoute une bille dans le tableau """
        self.board[y - 1][x - 1] = 1

    def delete_ball(self, x, y):
        """ Supprime une bille du tableau """
        self.board[y - 1][x - 1] = 0

    def load_from_file(self, filename):
        """ Charge un tableau à partir d'un fichier """
        with open(filename, "r") as file:
            for i in range(self.lines):
                line = file.readline()
                # fill line with zeros
                for j in range(self.columns - len(line)):
                    line += "0"
                for j in range(self.columns):
                    if line[j] == "O":
                        self.board[i][j] = 0
                    elif line[j] == "1":
                        self.board[i][j] = 1

    def count_balls(self):
        """ Compte le nombre de billes dans le tableau """
        nb_balls = 0
        for i in range(self.lines):
            for j in range(self.columns):
                if self.board[i][j] == 1:
                    nb_balls += 1
        return nb_balls

    def is_ball(self, x, y):
        """ Vérifie si une bille est présente à la position x, y """
        if x < 1 or x > self.columns:
            return False
        if y < 1 or y > self.lines:
            return False
        if self.board[y - 1][x - 1] == 1:
            return True
        return False

    def can_be_thrown(self, x, y, direction=""):
        """ Vérifie si la bille peut être lancée """
        """ c'est à dire si il y a pas une bille dans la direction """
        """ a au moins 2 cases de distance """
        """ et qu'elle ne sortira pas du tableau """
        if not self.is_ball(x, y):
            return False
        if direction == "up":
            if y > 2:
                if self.is_ball(x, y - 1):
                    return False
                for i in range(2, y):
                    if self.is_ball(x, y - i):
                        return True

        elif direction == "down":
            if y < self.lines - 1:
                if self.is_ball(x, y + 1):
                    return False
                for i in range(2, self.lines - y + 1):
                    if self.is_ball(x, y + i):
                        return True

        elif direction == "left":
            if x > 2:
                if self.is_ball(x - 1, y):
                    return False
                for i in range(2, x):
                    if self.is_ball(x - i, y):
                        return True

        elif direction == "right":
            if x < self.columns - 1:
                if self.is_ball(x + 1, y):
                    return False
                for i in range(2, self.columns - x + 1):
                    if self.is_ball(x + i, y):
                        return True
        return False

    def can_exit(self, x, y, direction=""):
        """ Vérifie si la bille peut sortir du tableau """
        if direction == "up":
            for i in range(1, y):
                if self.is_ball(x, i):
                    return False
        elif direction == "down":
            for i in range(y+1, self.lines + 1):
                if self.is_ball(x, i):
                    return False
        elif direction == "left":
            for i in range(1, x):
                if self.is_ball(i, y):
                    return False
        elif direction == "right":
            for i in range(x+1, self.columns + 1):
                if self.is_ball(i, y):
                    return False
        return True

    def move(self, x, y, direction=""):
        """ Déplace la bille dans la direction donnée """
        if direction == "up":
            i = 1
            while not self.is_ball(x, y - i):
                i += 1
            self.delete_ball(x, y)
            self.all_ball(x, y - i + 1)
            if self.can_exit(x, y-i, direction):
                self.delete_ball(x, y - i)
            else:
                self.move(x, y-i, direction)

        elif direction == "down":
            i = 1
            while not self.is_ball(x, y + i):
                i += 1
            self.delete_ball(x, y)
            self.all_ball(x, y + i - 1)
            if self.can_exit(x, y+i, direction):
                self.delete_ball(x, y + i)
            else:
                self.move(x, y+i, direction)

        elif direction == "left":
            i = 1
            while not self.is_ball(x - i, y):
                i += 1
            self.delete_ball(x, y)
            self.all_ball(x - i + 1, y)
            if self.can_exit(x-i, y, direction):
                self.delete_ball(x - i, y)
            else:
                self.move(x-i, y, direction)

        elif direction == "right":
            i = 1
            while not self.is_ball(x + i, y):
                i += 1
            self.delete_ball(x, y)
            self.all_ball(x + i - 1, y)
            if self.can_exit(x+i, y, direction):
                self.delete_ball(x + i, y)
            else:
                self.move(x+i, y, direction)

    def possible_moves(self):
        """ Construit le nombre de mouvements possibles """
        moves = []
        for i in range(1, self.lines + 1):
            for j in range(1, self.columns + 1):
                if self.can_be_thrown(j, i, "up"):
                    moves.append((j, i, "up"))
                if self.can_be_thrown(j, i, "down"):
                    moves.append((j, i, "down"))
                if self.can_be_thrown(j, i, "left"):
                    moves.append((j, i, "left"))
                if self.can_be_thrown(j, i, "right"):
                    moves.append((j, i, "right"))
        return moves

    def copy(self):
        """ Copie le tableau """
        tab = Board(self.lines, self.columns)
        for i in range(self.lines):
            for j in range(self.columns):
                tab.board[i][j] = self.board[i][j]
        return tab