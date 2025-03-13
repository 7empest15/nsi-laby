class Pile:
    """Classe Pile"""

    def __init__(self):
        """Initialisation d'une pile vide de type liste Python"""
        self.contenu=[]

    def est_vide(self):
        """Test si la pile est vide (retourne True) ou non (retourne False)"""
        return self.contenu==[]

    def empiler(self,x):
        """Empile un élément x au sommet de la pile"""
        self.contenu.append(x)

    def depiler(self):
        """Depile le sommet de la pile et le retourne"""
        if not self.est_vide():
            return self.contenu.pop()
        else:
            print("Pile vide !")
        """Autre méthode"""
        """assert not self.est_vide(),\"Pile vide !\""""
        """return self.contenu.pop()"""

    def taille(self):
        return len(self.contenu)

    def sommet(self):
        if not self.est_vide():
            return self.contenu[-1]
        else:
            print("Pile vide !")
