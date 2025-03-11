import pygame
from pygame.locals import *
from random import randint, choice
from sys import exit
from pile import *

class Case:
    def __init__(self):
        self.murN = True
        self.murS = True
        self.murW = True
        self.murE = True
        self.vue = False
        self.est_sortie = False  # Attribut pour indiquer si la case est une sortie
        self.direction_sortie = None  # Direction de la sortie (N, S, E, W)

class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.laby = []
        self.sortie = None  # Pour stocker les coordonnées de la sortie
        
        for ligne in range(self.largeur):
            self.laby.append([])
            for colonne in range(self.hauteur):
                colonne = Case()
                self.laby[ligne].append(colonne)
    
    def __directions_possibles(self, i, j):
        directions = []
        if j < self.hauteur - 1 and not self.laby[i][j + 1].vue:
            directions.append('S')
        if j > 0 and not self.laby[i][j - 1].vue:
            directions.append('N')
        if i < self.largeur - 1 and not self.laby[i + 1][j].vue:
            directions.append('E')
        if i > 0 and not self.laby[i - 1][j].vue:
            directions.append('W')
        return directions
    
    def __abattre_mur(self, i, j, dir, pile):
        if dir == 'S':
            self.laby[i][j].murS = False
            self.laby[i][j + 1].murN = False
            self.laby[i][j + 1].vue = True
            pile.empiler((i, j + 1))
        if dir == 'N':
            self.laby[i][j].murN = False
            self.laby[i][j - 1].murS = False
            self.laby[i][j - 1].vue = True
            pile.empiler((i, j - 1))
        if dir == 'W':
            self.laby[i][j].murW = False
            self.laby[i - 1][j].murE = False
            self.laby[i - 1][j].vue = True
            pile.empiler((i - 1, j))
        if dir == 'E':
            self.laby[i][j].murE = False
            self.laby[i + 1][j].murW = False
            self.laby[i + 1][j].vue = True
            pile.empiler((i + 1, j))
    
    def generer(self):
        # Marquer toutes les cases comme non visitées
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.laby[i][j].vue = False
                self.laby[i][j].est_sortie = False
                self.laby[i][j].direction_sortie = None
                
        pile = Pile()
        x = randint(0, self.largeur - 1)
        y = randint(0, self.hauteur - 1)
        self.laby[x][y].vue = True  # Marquer la première case comme visitée
        pile.empiler((x, y))
        
        while not pile.est_vide():
            case = pile.depiler()
            direction = self.__directions_possibles(case[0], case[1])
            if len(direction) > 0:
                pile.empiler((case[0], case[1]))
                direction_choose = choice(direction)
                self.__abattre_mur(case[0], case[1], direction_choose, pile)
    
    def generer_sortie(self):
        """Génère une sortie aléatoire sur le bord du labyrinthe.
        Retourne les coordonnées de la sortie sous forme de tuple (i, j) et la direction ('N', 'S', 'E', 'W')."""
        
        # Choisir aléatoirement un côté du labyrinthe
        cote = choice(['N', 'S', 'E', 'W'])
        
        if cote == 'N':  # Mur Nord
            i = randint(0, self.largeur - 1)
            j = 0
            self.laby[i][j].murN = False
            self.laby[i][j].est_sortie = True
            self.laby[i][j].direction_sortie = 'N'
            self.sortie = (i, j)
            return (i, j), 'N'
        
        elif cote == 'S':  # Mur Sud
            i = randint(0, self.largeur - 1)
            j = self.hauteur - 1
            self.laby[i][j].murS = False
            self.laby[i][j].est_sortie = True
            self.laby[i][j].direction_sortie = 'S'
            self.sortie = (i, j)
            return (i, j), 'S'
        
        elif cote == 'W':  # Mur Ouest
            i = 0
            j = randint(0, self.hauteur - 1)
            self.laby[i][j].murW = False
            self.laby[i][j].est_sortie = True
            self.laby[i][j].direction_sortie = 'W'
            self.sortie = (i, j)
            return (i, j), 'W'
        
        elif cote == 'E':  # Mur Est
            i = self.largeur - 1
            j = randint(0, self.hauteur - 1)
            self.laby[i][j].murE = False
            self.laby[i][j].est_sortie = True
            self.laby[i][j].direction_sortie = 'E'
            self.sortie = (i, j)
            return (i, j), 'E'
    
    def get_murs(self):
        """Retourne la liste des murs dans le format attendu par la fonction render."""
        murs = []
        for i in range(self.largeur):
            for j in range(self.hauteur):
                murs.append(((i, j), self.laby[i][j].murN, self.laby[i][j].murS, 
                           self.laby[i][j].murW, self.laby[i][j].murE))
        return murs
    
    def get_sortie(self):
        """Retourne les informations sur la sortie."""
        if self.sortie:
            i, j = self.sortie
            return (i, j), self.laby[i][j].direction_sortie
        return None, None
