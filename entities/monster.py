from .entity import Entity
import time
import random
import math
from collections import deque
from utils.logger import combat_logger, pathfind_logger
from utils.effects import effects

class Monster(Entity):
    def __init__(self, hp, time, atk_rate, atk, speed, range, pos_player):
        super().__init__(hp, time, atk_rate, atk, speed, range, pos_player)
        self.last_move = 0
        self.move_cooldown = 1000  # millisecondes
        self.target = None
        self.path = []
        self.last_attack = 0
        self.attack_cooldown = 2000  # 2 secondes entre les attaques
        self.attack_animation = 0
        self.is_attacking = False
        self.is_dead = False
        self.death_time = None
        self.color = (255, 0, 0, 255)  # Rouge avec alpha

    def set_target(self, target):
        self.target = target

    def can_move_to(self, new_pos, labyrinthe):
        i, j = new_pos
        if i < 0 or i >= labyrinthe.largeur or j < 0 or j >= labyrinthe.hauteur:
            return False
        
        # Vérifier les murs de la case actuelle
        current_case = labyrinthe.laby[self.pos[0]][self.pos[1]]
        if i > self.pos[0] and current_case.murE:  # Déplacement vers la droite
            return False
        if i < self.pos[0] and current_case.murW:  # Déplacement vers la gauche
            return False
        if j > self.pos[1] and current_case.murS:  # Déplacement vers le bas
            return False
        if j < self.pos[1] and current_case.murN:  # Déplacement vers le haut
            return False
            
        # Vérifier collision avec le joueur
        if self.target and self.target.pos[0] == i and self.target.pos[1] == j:
            return False
            
        # Vérifier collision avec les autres monstres
        if hasattr(self, 'labyrinthe'):
            for enemy in self.labyrinthe.level.enemies:
                if enemy != self and enemy.pos[0] == i and enemy.pos[1] == j:
                    return False
        
        return True

    def find_path(self, target_pos, labyrinthe):
        """Utilise BFS pour trouver le chemin le plus court vers la cible"""
        start = tuple(self.pos)
        target = tuple(target_pos)
        
        pathfind_logger.log(f"Recherche de chemin - Départ: {start}, Arrivée: {target}")
        
        # Si déjà à la cible, retourner un chemin vide
        if start == target:
            pathfind_logger.log("Déjà à la position cible")
            return []
            
        queue = deque([(start, [])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            # Vérifier les mouvements possibles
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                # Si c'est la cible, retourner le chemin
                if next_pos == target:
                    pathfind_logger.log(f"Chemin trouvé: {path + [next_pos]}")
                    return path + [next_pos]
                
                # Sinon, continuer la recherche
                if (next_pos not in visited and 
                    0 <= next_pos[0] < labyrinthe.largeur and 
                    0 <= next_pos[1] < labyrinthe.hauteur):
                    
                    # Sauvegarder la position actuelle
                    temp_pos = self.pos[:]
                    # Simuler le déplacement pour vérifier les murs
                    self.pos[0], self.pos[1] = current
                    
                    if self.can_move_to(next_pos, labyrinthe):
                        visited.add(next_pos)
                        new_path = path + [next_pos]
                        queue.append((next_pos, new_path))
                    
                    # Restaurer la position
                    self.pos[0], self.pos[1] = temp_pos
        
        pathfind_logger.log("Aucun chemin trouvé")
        return None

    def move_towards_target(self, labyrinthe):
        current_time = time.time() * 1000
        if not self.target or current_time - self.last_move < self.move_cooldown:
            return

        target_pos = self.target.pos
        dx = target_pos[0] - self.pos[0]
        dy = target_pos[1] - self.pos[1]
        distance = math.sqrt(dx*dx + dy*dy)

        # Vérifier si on peut attaquer (adjacent et pas de mur entre)
        if distance <= self.range and self.can_attack(self.target, labyrinthe):
            combat_logger.log(f"Monstre à portée d'attaque - Distance: {distance:.2f}, Position: {self.pos}")
            if current_time - self.last_attack >= self.attack_cooldown:
                self.start_attack(self.target)
            return

        # Trouver et suivre le chemin
        if not self.path:
            self.path = self.find_path(target_pos, labyrinthe)
            if not self.path:  # Si pas de chemin trouvé, essayer de se rapprocher
                possible_moves = []
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_pos = (self.pos[0] + dx, self.pos[1] + dy)
                    if self.can_move_to(new_pos, labyrinthe):
                        possible_moves.append(new_pos)
                if possible_moves:
                    self.path = [random.choice(possible_moves)]
                    pathfind_logger.log(f"Déplacement aléatoire vers: {self.path[0]}")
        
        if self.path:
            next_pos = self.path[0]
            if self.can_move_to(next_pos, labyrinthe):
                old_pos = self.pos[:]
                self.pos[0], self.pos[1] = next_pos
                self.path.pop(0)
                self.last_move = current_time
                pathfind_logger.log(f"Déplacement de {old_pos} vers {self.pos}")
            else:
                self.path = []
                pathfind_logger.log("Chemin bloqué, recalcul nécessaire")

    def can_attack(self, target, labyrinthe):
        # Vérifier si la cible est adjacente
        dx = abs(target.pos[0] - self.pos[0])
        dy = abs(target.pos[1] - self.pos[1])
        return (dx <= 1 and dy <= 1) and not self.is_wall_between(target.pos, labyrinthe)

    def is_wall_between(self, target_pos, labyrinthe):
        # Vérifier s'il y a un mur entre la position actuelle et la cible
        if self.pos[0] == target_pos[0]:  # Même colonne
            y = min(self.pos[1], target_pos[1])
            return (labyrinthe.laby[self.pos[0]][y].murS if self.pos[1] < target_pos[1] 
                   else labyrinthe.laby[self.pos[0]][target_pos[1]].murN)
        elif self.pos[1] == target_pos[1]:  # Même ligne
            x = min(self.pos[0], target_pos[0])
            return (labyrinthe.laby[x][self.pos[1]].murE if self.pos[0] < target_pos[0]
                   else labyrinthe.laby[target_pos[0]][self.pos[1]].murW)
        return True  # Séparés en diagonale

    def start_attack(self, target):
        current_time = time.time() * 1000
        time_since_last = current_time - self.last_attack
        combat_logger.log(f"Tentative d'attaque - Délai depuis dernière attaque: {time_since_last/1000:.2f}s")
        
        if current_time - self.last_attack >= self.attack_cooldown:
            combat_logger.log(f"Attaque autorisée - HP monstre: {self.hp}, HP cible avant: {target.hp}")
            self.is_attacking = True
            self.attack_animation = current_time
            self.last_attack = current_time
            self.attack(target, self.atk)
            combat_logger.log(f"Dégâts infligés: {self.atk}, HP cible après: {target.hp}")
        else:
            combat_logger.log("Attaque refusée - Cooldown non terminé")

    def attack(self, target, damage):
        combat_logger.log(f"Attaque - Dégâts prévus: {damage}")
        super().attack(target, damage)

    def update_attack_animation(self):
        if self.is_attacking:
            current_time = time.time() * 1000
            if current_time - self.attack_animation > 500:  # Durée de l'animation
                self.is_attacking = False

    def tick(self):
        if self.is_dead:
            return  # Ne rien faire si le monstre est mort
            
        if hasattr(self, 'labyrinthe'):
            current_time = time.time() * 1000
            # Se déplacer uniquement si pas en train d'attaquer
            if not self.is_attacking:
                self.move_towards_target(self.labyrinthe)
            self.update_attack_animation()

    def decrease_hp(self, damage):
        super().decrease_hp(damage)
        effects.play_hit_sound()
        if self.hp <= 0 and not self.is_dead:
            self.is_dead = True
            self.death_time = time.time() * 1000
            effects.play_death_sound()
            effects.create_death_effect(self.pos, self.color)
            combat_logger.log(f"Monstre mort à la position {self.pos}")

class Caecior(Monster):
    def __init__(self, hp, time, atk_rate, atk, speed, range, pos_player):
        super().__init__(hp, time, atk_rate, atk, speed, range, pos_player)
        self.fog_active = False
        self.fog_duration = 15000  # 15 secondes en millisecondes
        self.fog_start_time = 0
        self.attack_cooldown = 3000  # 3 secondes entre les attaques pour le Caecior
        self.color = (255, 165, 0, 255)  # Orange avec alpha

    def start_attack(self, target):
        super().start_attack(target)
        if not self.fog_active:
            self.activate_warfog()

    def activate_warfog(self):
        self.fog_active = True
        self.fog_start_time = time.time() * 1000
        combat_logger.log("Activation du brouillard de guerre")

    def tick(self):
        super().tick()
        if self.fog_active and time.time() * 1000 - self.fog_start_time > self.fog_duration:
            self.fog_active = False
            combat_logger.log("Désactivation du brouillard de guerre")