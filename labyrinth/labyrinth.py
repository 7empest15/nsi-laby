import pygame
from pygame.locals import *
from random import randint, choice
from sys import exit
from utils.pile import *

class Case:
    def __init__(self):
        self.murN = True
        self.murS = True
        self.murW = True
        self.murE = True
        self.vue = False


class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.laby = []
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
        pile = Pile()
        x = randint(0, self.largeur - 1)
        y = randint(0, self.hauteur - 1)
        pile.empiler((x, y))
        while not pile.est_vide():
            case = pile.depiler()
            direction = self.__directions_possibles(case[0], case[1])
            if len(direction) > 1:
                pile.empiler((case[0], case[1]))
            if direction:
                direction_choose = choice(direction)
                self.__abattre_mur(case[0], case[1], direction_choose, pile)

    def get_murs(self):
        murs = []
        for i in range(self.largeur):
            for j in range(self.hauteur):
                murs.append(((i, j), self.laby[i][j].murN, self.laby[i][j].murS, self.laby[i][j].murW, self.laby[i][j].murE))
        return murs


### Programme principal ###
if __name__ == '__main__':
    lab = Labyrinthe(100, 100)
    lab.generer()
    murs = lab.get_murs()
    for mur in murs:
        print(mur)