from .entity import Entity
from abilities.abilities import Abilities, AbilityType
import time
from utils.logger import combat_logger

class Player(Entity):
    def __init__(self, hp, time, atk_rate, atk, speed, range, pos_player, abilities=None):
        super().__init__(hp, time, atk_rate, atk, speed, range, pos_player)
        self.last_attack = 0
        self.attack_cooldown = 1000  # 1 seconde entre les attaques
        self.is_attacking = False
        self.abilities = Abilities(abilities)

    def can_attack(self, target, labyrinthe):
        # Vérifier si la cible est adjacente
        dx = abs(target.pos[0] - self.pos[0])
        dy = abs(target.pos[1] - self.pos[1])
        
        # Vérifier s'il y a un mur entre le joueur et la cible
        if dx <= 1 and dy <= 1:
            if self.pos[0] == target.pos[0]:  # Même colonne
                if self.pos[1] < target.pos[1]:  # Cible en dessous
                    return not labyrinthe.laby[self.pos[0]][self.pos[1]].murS
                else:  # Cible au-dessus
                    return not labyrinthe.laby[self.pos[0]][target.pos[1]].murN
            elif self.pos[1] == target.pos[1]:  # Même ligne
                if self.pos[0] < target.pos[0]:  # Cible à droite
                    return not labyrinthe.laby[self.pos[0]][self.pos[1]].murE
                else:  # Cible à gauche
                    return not labyrinthe.laby[target.pos[0]][self.pos[1]].murW
        return False

    def try_attack(self, enemies, labyrinthe):
        current_time = time.time() * 1000
        
        # Vérifier le cooldown
        if current_time - self.last_attack < self.attack_cooldown:
            combat_logger.log(f"Attaque impossible - Cooldown restant: {(self.attack_cooldown - (current_time - self.last_attack))/1000:.2f}s")
            return
        
        # Chercher un monstre adjacent
        for enemy in enemies:
            if self.can_attack(enemy, labyrinthe):
                combat_logger.log(f"Attaque du joueur - Position: {self.pos}, Cible: {enemy.pos}")
                self.is_attacking = True
                self.last_attack = current_time
                self.attack(enemy, self.atk)
                combat_logger.log(f"Dégâts infligés: {self.atk}, HP restants du monstre: {enemy.hp}")
                return
        
        combat_logger.log("Aucune cible à portée d'attaque")

    def tick(self, level, screen):
        self.abilities.apply(self, level, screen)
        super().tick()