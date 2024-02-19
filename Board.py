from configparser import ConfigParser


class Board():
    """ Représentation du tableau du jeu Fling """

    def __init__(self, lines=8, columns=7):
        """ Constructeur de la classe Tableau """
        constants = ConfigParser()
        constants.read("constants.ini")
        self.EMPTY = constants.getint("Board", "EMPTY")
        self.BALL = constants.getint("Board", "BALL")
        self.BABYBALL = constants.getint("Board", "BABYBALL")
        self.BIGBALL = constants.getint("Board", "BIGBALL")
        self.FROZEN = constants.getint("Board", "FROZEN")
        self.DOUBLEFROZEN = constants.getint("Board", "DOUBLEFROZEN")
        self.HOLE = constants.getint("Board", "HOLE")
        self.CRACKEDTILE = constants.getint("Board", "CRACKEDTILE")
        self.WALL = constants.getint("Board", "WALL")
        self.BREAKABLEWALL = constants.getint("Board", "BREAKABLEWALL")
        self.BOULDER = constants.getint("Board", "BOULDER")
        self.SHRINKER = constants.getint("Board", "SHRINKER")
        self.GROWER = constants.getint("Board", "GROWER")
        self.SANDTRAP = constants.getint("Board", "SANDTRAP")
        self.TRAPPEDBABYBALL = constants.getint("Board", "TRAPPEDBABYBALL")
        self.TRAPPEDBALL = constants.getint("Board", "TRAPPEDBALL")
        self.TRAPPEDBIGBALL = constants.getint("Board", "TRAPPEDBIGBALL")
        self.TRAPPEDBOULDER = constants.getint("Board", "TRAPPEDBOULDER")
        self.TELEPORT = constants.getint("Board", "TELEPORT")

        self.lines = lines
        self.columns = columns
        self.board = [[0 for i in range(columns)] for j in range(lines)]
        self.teleports = []

    def __str__(self):
        """ Affichage du tableau """
        my_string = ""
        for i in range(self.lines):
            for j in range(self.columns):
                match int(self.board[i][j]):
                    case self.EMPTY:
                        my_string += ". "
                    case self.BALL:
                        my_string += "O "
                    case self.WALL:
                        my_string += "W "
                    case self.BREAKABLEWALL:
                        my_string += "w "
                    case self.BABYBALL:
                        my_string += "o "
                    case self.BIGBALL:
                        my_string += "B "
                    case self.FROZEN:
                        my_string += "f "
                    case self.DOUBLEFROZEN:
                        my_string += "F "
                    case self.HOLE:
                        my_string += "X "
                    case self.CRACKEDTILE:
                        my_string += "x "
                    case self.BOULDER:
                        my_string += "d "
                    case self.SHRINKER:
                        my_string += "s "
                    case self.GROWER:
                        my_string += "g "
                    case self.SANDTRAP:
                        my_string += "S "
                    case self.TRAPPEDBABYBALL:
                        my_string += "So"
                    case self.TRAPPEDBALL:
                        my_string += "SO"
                    case self.TRAPPEDBIGBALL:
                        my_string += "SB"
                    case self.TRAPPEDBOULDER:
                        my_string += "Sd"
            my_string += "\n"
        my_string_list = list(my_string)
        if len(self.teleports) == 2:
            my_string_list[(self.teleports[0][1] - 1) * (self.columns * 2 + 1) + (self.teleports[0][0] - 1) * 2 + 1] = my_string_list[(self.teleports[0][1] - 1) * (self.columns * 2 + 1) + (self.teleports[0][0] - 1) * 2]
            my_string_list[(self.teleports[0][1] - 1) * (self.columns * 2 + 1) + (self.teleports[0][0] - 1) * 2] = "T"
            my_string_list[(self.teleports[1][1] - 1) * (self.columns * 2 + 1) + (self.teleports[1][0] - 1) * 2 + 1] = my_string_list[(self.teleports[1][1] - 1) * (self.columns * 2 + 1) + (self.teleports[1][0] - 1) * 2]
            my_string_list[(self.teleports[1][1] - 1) * (self.columns * 2 + 1) + (self.teleports[1][0] - 1) * 2] = "T"
        my_string = "".join(my_string_list)
        return my_string

    def get_id(self):
        """ Retourne l'identifiant du tableau """
        """ C'est un nombre binaire formé par la concaténation des lignes """
        """ du tableau """
        id = ""
        for i in range(self.lines):
            for j in range(self.columns):
                id += chr(self.board[i][j] + 48)
        if len(self.teleports):
            id += str(self.teleports[0][0])
            id += str(self.teleports[0][1])
            id += str(self.teleports[1][0])
            id += str(self.teleports[1][1])
        else:
            id += "0000"
        return id

    def set_id(self, id):
        """ Initialise le tableau à partir de son identifiant """
        """ On transforme le nombre en binaire et on place les 1 comme billes dans le tableau """
        id_tmp = id
        for i in range(self.lines):
            for j in range(self.columns):
                char = id_tmp[i * self.columns + j]
                self.board[i][j] = ord(char) - 48
        """ if 4 last characters are not 0, we have teleports """
        if int(id_tmp[self.lines * self.columns]) != 0:
            self.teleports = [(int(id_tmp[self.lines * self.columns]), int(id_tmp[self.lines * self.columns + 1])),
                              (int(id_tmp[self.lines * self.columns + 2]), int(id_tmp[self.lines * self.columns + 3]))]

    def add_ball(self, x, y, type=None):
        type_n = type
        if type is None:
            type_n = self.BALL

        """ Ajoute une bille dans le tableau """
        self.board[y - 1][x - 1] = type_n

    def delete_ball(self, x, y):
        """ Supprime une bille du tableau """
        self.board[y - 1][x - 1] = 0

    def get_element(self, x, y):
        """ Retourne l'élément du tableau à la position x, y """
        return self.board[y - 1][x - 1]

    def set_element(self, x, y, element=None):
        """ Initialise l'élément du tableau à la position x, y """
        if element is None:
            element = self.EMPTY
        self.board[y - 1][x - 1] = element

    def load_from_file(self, filename):
        """ Charge un tableau à partir d'un fichier """
        with open(filename, "r") as file:
            for i in range(self.lines):
                line = file.readline()
                # fill line with zeros
                for j in range(self.columns - len(line)):
                    line += "0"
                for j in range(self.columns):
                    match line[j]:
                        case "0":
                            self.board[i][j] = self.EMPTY
                        case "1":
                            self.board[i][j] = self.BALL
                        case "W":
                            self.board[i][j] = self.WALL
                        case "w":
                            self.board[i][j] = self.BREAKABLEWALL
                        case "b":
                            self.board[i][j] = self.BABYBALL
                        case "B":
                            self.board[i][j] = self.BIGBALL
                        case "f":
                            self.board[i][j] = self.FROZEN
                        case "F":
                            self.board[i][j] = self.DOUBLEFROZEN
                        case "X":
                            self.board[i][j] = self.HOLE
                        case "x":
                            self.board[i][j] = self.CRACKEDTILE
                        case "d":
                            self.board[i][j] = self.BOULDER
                        case "s":
                            self.board[i][j] = self.SHRINKER
                        case "g":
                            self.board[i][j] = self.GROWER
                        case "S":
                            self.board[i][j] = self.SANDTRAP
                        case "t":
                            self.teleports.append((j + 1, i + 1))

    def count_balls(self):
        """ Compte le nombre de billes dans le tableau """
        nb_balls = 0
        for i in range(self.lines):
            for j in range(self.columns):
                if (self.board[i][j] == self.BALL or
                        self.board[i][j] == self.BABYBALL or
                        self.board[i][j] == self.BIGBALL or
                        self.board[i][j] == self.TRAPPEDBABYBALL or
                        self.board[i][j] == self.TRAPPEDBALL or
                        self.board[i][j] == self.TRAPPEDBIGBALL or
                        self.board[i][j] == self.FROZEN or
                        self.board[i][j] == self.DOUBLEFROZEN):
                    nb_balls += 1
        return nb_balls

    def is_in_board(self, x, y):
        """ Vérifie si la position x, y est dans le tableau """
        if x < 1 or x > self.columns:
            return False
        if y < 1 or y > self.lines:
            return False
        return True

    def is_ball(self, x, y):
        """ Vérifie si une bille est présente à la position x, y """
        if (self.is_in_board(x, y) and
                (self.get_element(x, y) == self.BALL
                 or self.get_element(x, y) == self.BABYBALL
                 or self.get_element(x, y) == self.BIGBALL
                 or self.get_element(x, y) == self.BOULDER
                 or self.get_element(x, y) == self.TRAPPEDBABYBALL
                 or self.get_element(x, y) == self.TRAPPEDBALL
                 or self.get_element(x, y) == self.TRAPPEDBIGBALL
                 or self.get_element(x, y) == self.TRAPPEDBOULDER)):
            return True
        return False

    def is_wall(self, x, y):
        """ Vérifie si un mur est présent à la position x, y """
        if self.is_in_board(x, y) and self.get_element(x, y) == self.WALL:
            return True
        return False

    def is_frozen(self, x, y):
        """ Vérifie si une bille est gelée à la position x, y """
        if self.is_in_board(x, y) and (
                self.get_element(x, y) == self.FROZEN or self.get_element(x, y) == self.DOUBLEFROZEN):
            return True
        return False

    def unfreeze(self, x, y):
        """ Décongèle une bille à la position x, y """
        if self.is_frozen(x, y):
            if self.get_element(x, y) == self.FROZEN:
                self.set_element(x, y, self.BALL)
            elif self.get_element(x, y) == self.DOUBLEFROZEN:
                self.set_element(x, y, self.FROZEN)

    def change_ball_size(self, ball, transformation):
        """ Change la taille de la bille """
        """ Change l'état de la bille à la position x, y """
        """ Décongèle une bille à la position x, y """
        if transformation == "shrink":
            if ball == self.BALL:
                return self.BABYBALL
            elif ball == self.BIGBALL:
                return self.BALL
            else:
                return ball
        elif transformation == "grow":
            if ball == self.BALL:
                return self.BIGBALL
            elif ball == self.BABYBALL:
                return self.BALL
            else:
                return ball

    def is_empty(self, x, y):
        """ Vérifie si la position x, y est vide """
        if self.is_in_board(x, y) and self.get_element(x, y) == self.EMPTY:
            return True
        return False
    def is_obstacle(self, x, y):
        return (self.is_ball(x, y) or
                self.is_wall(x, y) or
                self.is_frozen(x, y) or
                self.get_element(x, y) == self.BREAKABLEWALL or
                self.get_element(x, y) == self.BOULDER)

    def is_teleport(self, x, y):
        if len(self.teleports) != 2:
            return False
        return self.teleports[0] == (x, y) or self.teleports[1] == (x, y)

    def is_trapped(self, x, y):
        """ Vérifie si une bille est piégée dans un bac à sable """
        return (self.get_element(x, y) == self.TRAPPEDBABYBALL or
                self.get_element(x, y) == self.TRAPPEDBALL or
                self.get_element(x, y) == self.TRAPPEDBIGBALL or
                self.get_element(x, y) == self.TRAPPEDBOULDER)

    def is_trapped_state(self, ball):
        """ Vérifie si une bille est dans un état piégé """
        return (ball == self.TRAPPEDBABYBALL or
                ball == self.TRAPPEDBALL or
                ball == self.TRAPPEDBIGBALL or
                ball == self.TRAPPEDBOULDER)

    def can_be_thrown(self, x, y, direction=""):
        """ Vérifie si la bille peut être lancée """
        """ c'est à dire si il y a pas une bille dans la direction """
        """ a au moins 2 cases de distance """
        """ et qu'elle ne sortira pas du tableau """
        if not self.is_ball(x, y):
            return False
        if direction == "up":
            if y > 2:
                i = 1
                if self.is_obstacle(x, y - i):
                    return False
                while y - i >= 0:
                    if self.is_obstacle(x, y - i):
                        return True
                    if self.is_teleport(x, y - i):
                        teleport_out = self.teleports[0] if (x, y - i) == self.teleports[1] else self.teleports[1]
                        x = teleport_out[0]
                        y = teleport_out[1]
                        if self.is_ball(x, y):
                            return True
                        i = 0
                    if self.get_element(x, y - i) == self.HOLE:
                        return False
                    if y > i and self.get_element(x, y - i) == self.SANDTRAP:
                        return True
                    i += 1

        elif direction == "down":
            if y < self.lines - 1:
                i = 1
                if self.is_obstacle(x, y + i):
                    return False
                while y + i <= self.lines:
                    if self.is_obstacle(x, y + i):
                        return True
                    if self.is_teleport(x, y + i):
                        teleport_out = self.teleports[0] if (x, y + i) == self.teleports[1] else self.teleports[1]
                        x = teleport_out[0]
                        y = teleport_out[1]
                        if self.is_ball(x, y):
                            return True
                        i = 0
                    if self.get_element(x, y + i) == self.HOLE:
                        return False
                    if y + i <= self.lines and self.get_element(x, y + i) == self.SANDTRAP:
                        return True
                    i += 1

        elif direction == "left":
            if x > 2:
                i = 1
                if self.is_obstacle(x - i, y):
                    return False
                while x - i >= 0:
                    if self.is_obstacle(x - i, y):
                        return True
                    if self.is_teleport(x - i, y):
                        teleport_out = self.teleports[0] if (x - i, y) == self.teleports[1] else self.teleports[1]
                        x = teleport_out[0]
                        y = teleport_out[1]
                        if self.is_ball(x, y):
                            return True
                        i = 0
                    if self.get_element(x - i, y) == self.HOLE:
                        return False
                    if x > i and self.get_element(x - i, y) == self.SANDTRAP:
                        return True
                    i += 1

        elif direction == "right":
            if x < self.columns - 1:
                i = 1
                if self.is_obstacle(x + i, y):
                    return False
                while x + i <= self.columns:
                    if self.is_obstacle(x + i, y):
                        return True
                    if self.is_teleport(x + i, y):
                        teleport_out = self.teleports[0] if (x + i, y) == self.teleports[1] else self.teleports[1]
                        x = teleport_out[0]
                        y = teleport_out[1]
                        if self.is_ball(x, y):
                            return True
                        i = 0
                    if self.get_element(x + i, y) == self.HOLE:
                        return False
                    if x + i < self.columns and self.get_element(x + i, y) == self.SANDTRAP:
                        return True
                    i += 1
        return False

    def can_be_played(self, x, y, direction=""):
        if (not self.is_ball(x, y) or
                self.get_element(x, y) == self.BABYBALL or
                self.get_element(x, y) == self.BOULDER or
                self.is_trapped(x, y)):
            return False
        return self.can_be_thrown(x, y, direction)

    def can_exit(self, x, y, direction=""):
        """ Vérifie si la bille peut sortir du tableau """
        if not self.is_ball(x, y):
            return False
        if direction == "up":
            i = y - 1
            while i > 0:
                if self.get_element(x, i) == self.HOLE:
                    return True
                if self.is_obstacle(x, i) or self.get_element(x, i) == self.SANDTRAP:
                    return False
                if self.is_teleport(x, i):
                    teleport_out = self.teleports[0] if (x, i) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y = teleport_out[1]
                    i = y
                i -= 1
        elif direction == "down":
            i = y + 1
            while i <= self.lines:
                if self.get_element(x, i) == self.HOLE:
                    return True
                if self.is_obstacle(x, i) or self.get_element(x, i) == self.SANDTRAP:
                    return False
                if self.is_teleport(x, i):
                    teleport_out = self.teleports[0] if (x, i) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y = teleport_out[1]
                    i = y
                i += 1
        elif direction == "left":
            i = x - 1
            while i > 0:
                if self.get_element(i, y) == self.HOLE:
                    return True
                if self.is_obstacle(i, y) or self.get_element(i, y) == self.SANDTRAP:
                    return False
                if self.is_teleport(i, y):
                    teleport_out = self.teleports[0] if (i, y) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y = teleport_out[1]
                    i = x
                i -= 1
        elif direction == "right":
            i = x + 1
            while i <= self.columns:
                if self.get_element(i, y) == self.HOLE:
                    return True
                if self.is_obstacle(i, y) or self.get_element(i, y) == self.SANDTRAP:
                    return False
                if self.is_teleport(i, y):
                    teleport_out = self.teleports[0] if (i, y) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y = teleport_out[1]
                    i = x
                i += 1
        return True

    def compare_size(self, element1, element2):
        """ Compare la taille de deux billes """
        weights = {
            self.BALL: 1,
            self.BABYBALL: 0,
            self.BIGBALL: 2,
            self.BOULDER: 1,
            self.TRAPPEDBABYBALL: 0,
            self.TRAPPEDBALL: 1,
            self.TRAPPEDBIGBALL: 2,
            self.TRAPPEDBOULDER: 1
        }
        return weights[element1] >= weights[element2]

    def trap_ball(self, ball):
        """ Piège une bille dans un bac à sable """
        if ball == self.BALL:
            return self.TRAPPEDBALL
        elif ball == self.BABYBALL:
            return self.TRAPPEDBABYBALL
        elif ball == self.BIGBALL:
            return self.TRAPPEDBIGBALL
        elif ball == self.BOULDER:
            return self.TRAPPEDBOULDER

    def eject_ball(self, x, y, direction):
        """ Éjecte une bille """
        if self.can_exit(x, y, direction):
            if direction == "up":
                y1 = y
                while y1 > 0:
                    if self.get_element(x, y1) == self.HOLE:
                        self.delete_ball(x, y)
                        return
                    if self.get_element(x, y1) == self.CRACKEDTILE:
                        self.set_element(x, y1, self.HOLE)
                    if self.get_element(x, y1) == self.SHRINKER or self.get_element(x, y1) == self.GROWER:
                        self.set_element(x, y1, self.EMPTY)
                    if y1 != y and self.is_teleport(x, y1):
                        teleport_out = self.teleports[0] if (x, y1) == self.teleports[1] else self.teleports[1]
                        self.eject_ball(teleport_out[0], teleport_out[1], direction)
                    y1 -= 1
            elif direction == "down":
                y1 = y
                while y1 <= self.lines:
                    if self.get_element(x, y1) == self.HOLE:
                        self.delete_ball(x, y)
                        return
                    if self.get_element(x, y1) == self.CRACKEDTILE:
                        self.set_element(x, y1, self.HOLE)
                    if self.get_element(x, y1) == self.SHRINKER or self.get_element(x, y1) == self.GROWER:
                        self.set_element(x, y1, self.EMPTY)
                    if y1 != y and self.is_teleport(x, y1):
                        teleport_out = self.teleports[0] if (x, y1) == self.teleports[1] else self.teleports[1]
                        self.eject_ball(teleport_out[0], teleport_out[1], direction)
                    y1 += 1
            elif direction == "left":
                x1 = x
                while x1 > 0:
                    if self.get_element(x1, y) == self.HOLE:
                        self.delete_ball(x, y)
                        return
                    if self.get_element(x1, y) == self.CRACKEDTILE:
                        self.set_element(x1, y, self.HOLE)
                    if self.get_element(x1, y) == self.SHRINKER or self.get_element(x1, y) == self.GROWER:
                        self.set_element(x1, y, self.EMPTY)
                    if x1 != x and self.is_teleport(x1, y):
                        teleport_out = self.teleports[0] if (x1, y) == self.teleports[1] else self.teleports[1]
                        self.eject_ball(teleport_out[0], teleport_out[1], direction)
                    x1 -= 1
            elif direction == "right":
                x1 = x
                while x1 <= self.columns:
                    if self.get_element(x1, y) == self.HOLE:
                        self.delete_ball(x, y)
                        return
                    if self.get_element(x1, y) == self.CRACKEDTILE:
                        self.set_element(x1, y, self.HOLE)
                    if self.get_element(x1, y) == self.SHRINKER or self.get_element(x1, y) == self.GROWER:
                        self.set_element(x1, y, self.EMPTY)
                    if x1 != x and self.is_teleport(x1, y):
                        teleport_out = self.teleports[0] if (x1, y) == self.teleports[1] else self.teleports[1]
                        self.eject_ball(teleport_out[0], teleport_out[1], direction)
                    x1 += 1
            self.delete_ball(x, y)
            return

    def move(self, x, y, direction=""):
        ball = self.get_element(x, y)
        cases = []
        """ Déplace la bille dans la direction donnée """
        if not self.is_ball(x, y):
            return
        if direction == "up":
            y0 = y
            while y0 > 0:
                cases.append((x, y0))
                y0 -= 1
                if self.is_teleport(x, y0):
                    cases.append((x, y0))
                    teleport_out = self.teleports[0] if (x, y0) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y0 = teleport_out[1]
                if self.is_obstacle(x, y0):
                    cases.append((x, y0))
                    break
        elif direction == "down":
            y0 = y
            while y0 <= self.lines:
                cases.append((x, y0))
                y0 += 1
                if self.is_teleport(x, y0):
                    cases.append((x, y0))
                    teleport_out = self.teleports[0] if (x, y0) == self.teleports[1] else self.teleports[1]
                    x = teleport_out[0]
                    y0 = teleport_out[1]
                if y0 <= self.lines and self.is_obstacle(x, y0):
                    cases.append((x, y0))
                    break
        elif direction == "left":
            x0 = x
            while x0 > 0:
                cases.append((x0, y))
                x0 -= 1
                if self.is_teleport(x0, y):
                    cases.append((x0, y))
                    teleport_out = self.teleports[0] if (x0, y) == self.teleports[1] else self.teleports[1]
                    x0 = teleport_out[0]
                    y = teleport_out[1]
                if self.is_obstacle(x0, y):
                    cases.append((x0, y))
                    break
        elif direction == "right":
            x0 = x
            while x0 <= self.columns:
                cases.append((x0, y))
                x0 += 1
                if self.is_teleport(x0, y):
                    cases.append((x0, y))
                    teleport_out = self.teleports[0] if (x0, y) == self.teleports[1] else self.teleports[1]
                    x0 = teleport_out[0]
                    y = teleport_out[1]
                if x0 <= self.columns and self.is_obstacle(x0, y):
                    cases.append((x0, y))
                    break

        cracked_to_holes = []

        for i in range(len(cases)-1):
            if self.get_element(cases[i+1][0], cases[i+1][1]) == self.CRACKEDTILE:
                cracked_to_holes.append(cases[i+1])
                self.add_ball(cases[i+1][0], cases[i+1][1], ball)
                self.delete_ball(cases[i][0], cases[i][1])
            elif self.is_empty(cases[i+1][0], cases[i+1][1]):
                self.add_ball(cases[i+1][0], cases[i+1][1], ball)
                self.delete_ball(cases[i][0], cases[i][1])
            elif self.is_ball(cases[i+1][0], cases[i+1][1]) and self.compare_size(ball, self.get_element(cases[i+1][0], cases[i+1][1])):
                if self.can_exit(cases[i+1][0], cases[i+1][1], direction):
                    if self.is_trapped(cases[i+1][0], cases[i+1][1]):
                        self.set_element(cases[i+1][0], cases[i+1][1], self.SANDTRAP)
                    else:
                        self.eject_ball(cases[i+1][0], cases[i+1][1], direction)
                        break
                else:
                    self.move(cases[i+1][0], cases[i+1][1], direction)
                break
            elif self.is_frozen(cases[i+1][0], cases[i+1][1]):
                self.unfreeze(cases[i+1][0], cases[i+1][1])
            elif self.get_element(cases[i+1][0], cases[i+1][1]) == self.BREAKABLEWALL:
                self.set_element(cases[i+1][0], cases[i+1][1], self.EMPTY)
            elif self.get_element(cases[i+1][0], cases[i+1][1]) == self.SHRINKER:
                ball = self.change_ball_size(ball, "shrink")
                self.add_ball(cases[i+1][0], cases[i+1][1], ball)
                self.delete_ball(cases[i][0], cases[i][1])
            elif self.get_element(cases[i+1][0], cases[i+1][1]) == self.GROWER:
                ball = self.change_ball_size(ball, "grow")
                self.add_ball(cases[i+1][0], cases[i+1][1], ball)
                self.delete_ball(cases[i][0], cases[i][1])
            elif self.get_element(cases[i+1][0], cases[i+1][1]) == self.SANDTRAP:
                ball = self.trap_ball(ball)
                self.add_ball(cases[i+1][0], cases[i+1][1], ball)
                self.delete_ball(cases[i][0], cases[i][1])
                break

        for i in range(len(cracked_to_holes)):
            self.set_element(cracked_to_holes[i][0], cracked_to_holes[i][1], self.HOLE)

    def possible_moves(self):
        """ Construit le nombre de mouvements possibles """
        moves = []
        for i in range(1, self.lines + 1):
            for j in range(1, self.columns + 1):
                for direction in ["up", "down", "left", "right"]:
                    # if self.is_ball(j, i):
                    #     print(f"can be thrown {j} {i} {direction} : {self.can_be_thrown(j, i, direction)}")
                    if self.can_be_played(j, i, direction):
                        moves.append((j, i, direction))
        return moves

    def copy(self):
        """ Copie le tableau """
        tab = Board(self.lines, self.columns)
        for i in range(self.lines):
            for j in range(self.columns):
                tab.board[i][j] = self.board[i][j]
        tab.teleports = self.teleports
        return tab
