from random import randint
from entities.monster import Monster, Caecior
from labyrinth.labyrinth import Labyrinthe
from entities.medkit import Medkit
import pygame
import time
from collections import deque

class Level:
    # Constantes pour l'équilibrage du jeu
    BASE_TIME = 120  # Temps de base en secondes
    TIME_PER_LEVEL = 30  # Temps supplémentaire par niveau
    MAX_MONSTERS = 5  # Nombre maximum de monstres normaux
    MAX_CAECIORS = 3  # Nombre maximum de Caeciors
    MAX_MEDKIT = 5
    BASE_MONSTER_HP = 30  # Points de vie de base des monstres
    BASE_MONSTER_DAMAGE = 10  # Dégâts de base des monstres
    HP_INCREASE_PER_LEVEL = 5  # Augmentation des PV par niveau
    DAMAGE_INCREASE_PER_LEVEL = 2  # Augmentation des dégâts par niveau

    def __init__(self, labyrinthe, player, exit_coordonnee, player_coordonnee, difficulty=1):
        self.labyrinthe = labyrinthe
        self.labyrinthe.level = self
        self.player = player
        self.enemies = []
        self.medkits = []
        self.exit_coordonnee = exit_coordonnee
        self.player_coordonnee = player_coordonnee
        self.player.pos = list(player_coordonnee)
        self.difficulty = difficulty
        self.kills = 0
        self.path_to_exit = []  # Stocke le chemin vers la sortie
        
        # Initialiser le niveau
        self.reset_level()

    def find_path_to_exit(self, start_pos=None):
        """Trouve le chemin le plus court vers la sortie"""
        if start_pos is None:
            start_pos = tuple(self.player.pos)
        target = tuple(self.exit_coordonnee)
        
        # Si déjà à la sortie, retourner un chemin vide
        if start_pos == target:
            return []
            
        queue = deque([(start_pos, [])])
        visited = {start_pos}
        
        def can_move_to(current, next_pos):
            i, j = current
            ni, nj = next_pos
            
            if ni < 0 or ni >= self.labyrinthe.largeur or nj < 0 or nj >= self.labyrinthe.hauteur:
                return False
                
            current_case = self.labyrinthe.laby[i][j]
            if ni > i and current_case.murE:  # Déplacement vers la droite
                return False
            if ni < i and current_case.murW:  # Déplacement vers la gauche
                return False
            if nj > j and current_case.murS:  # Déplacement vers le bas
                return False
            if nj < j and current_case.murN:  # Déplacement vers le haut
                return False
            return True
        
        while queue:
            current, path = queue.popleft()
            
            # Vérifier les mouvements possibles
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if next_pos == target:
                    return path + [next_pos]
                
                if next_pos not in visited and can_move_to(current, next_pos):
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
        
        return []  # Pas de chemin trouvé

    def reset_level(self):
        """Réinitialise le niveau actuel sans changer la difficulté"""
        # Réinitialiser le temps
        self.time_remaining = self.BASE_TIME + (self.difficulty * self.TIME_PER_LEVEL)
        self.last_tick = time.time()
        
        # Vider la liste des ennemis
        self.enemies.clear()
        
        # Recréer un nouveau labyrinthe avec les mêmes dimensions
        self.labyrinthe = Labyrinthe(self.labyrinthe.largeur, self.labyrinthe.hauteur)
        self.labyrinthe.level = self
        self.labyrinthe.generer()
        
        # Marquer la sortie
        self.mark_exit()
        
        # Replacer le joueur au début
        self.player.pos = list(self.player_coordonnee)
        
        # Calculer le chemin vers la sortie
        self.path_to_exit = self.find_path_to_exit()
        
        # Spawn des ennemis
        self.spawn_enemies()
        self.spawn_medkits()

    def spawn_enemies(self):
        """Génère les ennemis pour le niveau actuel"""
        # Calculer le nombre de monstres basé sur la difficulté, avec un maximum
        num_monsters = min(self.difficulty + 1, self.MAX_MONSTERS)
        num_caeciors = min(self.difficulty // 2, self.MAX_CAECIORS)
        
        # Calculer les stats des monstres pour ce niveau
        monster_hp = self.BASE_MONSTER_HP + (self.difficulty * self.HP_INCREASE_PER_LEVEL)
        monster_damage = self.BASE_MONSTER_DAMAGE + (self.difficulty * self.DAMAGE_INCREASE_PER_LEVEL)
        
        # Spawn des monstres normaux
        for _ in range(num_monsters):
            self.spawn_enemy(Monster, monster_hp, 1, monster_damage, 1, 1)
            
        # Spawn des Caeciors (plus forts)
        for _ in range(num_caeciors):
            caecior_hp = int(monster_hp * 1.5)
            caecior_damage = int(monster_damage * 1.2)
            self.spawn_enemy(Caecior, caecior_hp, 1, caecior_damage, 1, 1)

    def spawn_enemy(self, enemy_type, hp, atk_rate, atk, speed, range):
        """Spawn un ennemi à une position valide"""
        # Nombre maximum de tentatives pour trouver une position valide
        max_attempts = 50
        attempts = 0
        
        while attempts < max_attempts:
            x = randint(0, self.labyrinthe.largeur - 1)
            y = randint(0, self.labyrinthe.hauteur - 1)
            
            # Vérifier la distance par rapport au joueur et à la sortie
            player_dist = abs(x - self.player_coordonnee[0]) + abs(y - self.player_coordonnee[1])
            exit_dist = abs(x - self.exit_coordonnee[0]) + abs(y - self.exit_coordonnee[1])
            
            # Vérifier qu'il n'y a pas déjà un monstre à cette position
            position_occupied = any(enemy.pos[0] == x and enemy.pos[1] == y for enemy in self.enemies)
            
            if player_dist > 5 and exit_dist > 5 and not position_occupied:
                enemy = enemy_type(hp, 0, atk_rate, atk, speed, range, (x, y))
                self.enemies.append(enemy)
                return True
                
            attempts += 1
        
        return False

    def spawn_medkits(self):
        """Génère les soins pour le niveau actuel"""
        # Calculer le nombre de monstres basé sur la difficulté, avec un maximum
        num_medkits = min(self.difficulty + 1, self.MAX_MEDKIT)
        print("Num medkits " + str(num_medkits))
        
        # Spawn des monstres normaux
        for _ in range(num_medkits):
            self.spawn_medkit(15)
            

    def spawn_medkit(self, quantity):
        max_attempts = 50
        attempts = 0
        
        while attempts < max_attempts:
            x = randint(0, self.labyrinthe.largeur - 1)
            y = randint(0, self.labyrinthe.hauteur - 1)
            
            # Vérifier la distance par rapport au joueur et à la sortie
            player_dist = abs(x - self.player_coordonnee[0]) + abs(y - self.player_coordonnee[1])
            exit_dist = abs(x - self.exit_coordonnee[0]) + abs(y - self.exit_coordonnee[1])
            
            # Vérifier qu'il n'y a pas déjà un monstre à cette position
            position_occupied = any(enemy.pos[0] == x and enemy.pos[1] == y for enemy in self.enemies)
            
            if player_dist > 5 and exit_dist > 5 and not position_occupied:
                medkit = Medkit(quantity, (x, y))
                self.medkits.append(medkit)
                print("Medkit spawned")
                return True
                
            attempts += 1
        
        
        return False

    def next_level(self):
        """Passe au niveau suivant"""
        # Augmenter la difficulté
        self.difficulty += 1
        
        # Réinitialiser le niveau avec la nouvelle difficulté
        self.reset_level()

    def reset(self):
        """Réinitialise complètement le jeu au niveau 1"""
        self.difficulty = 1
        self.kills = 0
        self.reset_level()

    def mark_exit(self):
        """Marque la sortie dans le labyrinthe"""
        self.labyrinthe.laby[self.exit_coordonnee[0]][self.exit_coordonnee[1]].is_exit = True

    def tick(self):
        """Met à jour l'état du niveau"""
        # Mettre à jour le timer
        current_time = time.time()
        elapsed = current_time - self.last_tick
        self.time_remaining = max(0, self.time_remaining - elapsed)
        self.last_tick = current_time
        
        # Mettre à jour le compteur de kills et nettoyer les ennemis morts
        old_enemy_count = len(self.enemies)
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
        self.kills += old_enemy_count - len(self.enemies)
        
        # Mettre à jour les ennemis restants
        for enemy in self.enemies:
            enemy.tick()

    def timer_end(self):
        if self.time_remaining <= 0:
            self.player.death()

    def win(self):
        if self.player_coordonnee == self.exit_coordonnee:
            print("win")