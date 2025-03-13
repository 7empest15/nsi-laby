from random import randint
from entities.monster import Monster, Caecior
import pygame
import time

class Level:
    def __init__(self, labyrinthe, player, exit_coordonnee, player_coordonnee, difficulty=1):
        self.labyrinthe = labyrinthe
        self.labyrinthe.level = self
        self.player = player
        self.enemies = []
        self.time_remaining = 120 + (difficulty * 30)  # Plus de temps pour les niveaux plus difficiles
        self.last_tick = time.time()
        self.exit_coordonnee = exit_coordonnee
        self.player_coordonnee = player_coordonnee
        self.player.pos = list(player_coordonnee)
        self.difficulty = difficulty
        self.kills = 0
        
        # Mark the exit in the labyrinth
        self.mark_exit()
        
        # Spawn enemies based on difficulty
        self.spawn_enemies()

    def mark_exit(self):
        # This will be used by the render function to show the exit
        self.labyrinthe.laby[self.exit_coordonnee[0]][self.exit_coordonnee[1]].is_exit = True

    def spawn_enemies(self):
        # Nombre de monstres basé sur la difficulté
        num_monsters = self.difficulty + 1
        num_caeciors = self.difficulty // 2
        
        # Stats de base des monstres
        base_hp = 30 + (self.difficulty * 5)  # HP augmente avec la difficulté
        base_damage = 10 + (self.difficulty * 2)  # Dégâts augmentent avec la difficulté
        
        # Spawn des monstres normaux
        for _ in range(num_monsters):
            self.spawn_enemy(Monster, base_hp, 1, base_damage, 1, 1)
            
        # Spawn des Caeciors
        for _ in range(num_caeciors):
            self.spawn_enemy(Caecior, base_hp * 1.5, 1, base_damage * 1.2, 1, 1)

    def spawn_enemy(self, enemy_type, hp, atk_rate, atk, speed, range):
        # Find a valid spawn position (not too close to player or exit)
        while True:
            x = randint(0, self.labyrinthe.largeur - 1)
            y = randint(0, self.labyrinthe.hauteur - 1)
            
            # Check distance from player and exit
            player_dist = abs(x - self.player_coordonnee[0]) + abs(y - self.player_coordonnee[1])
            exit_dist = abs(x - self.exit_coordonnee[0]) + abs(y - self.exit_coordonnee[1])
            
            if player_dist > 5 and exit_dist > 5:  # Minimum distance of 5 cells
                enemy = enemy_type(hp, 0, atk_rate, atk, speed, range, (x, y))
                self.enemies.append(enemy)
                break

    def tick(self):
        # Update timer using real time
        current_time = time.time()
        elapsed = current_time - self.last_tick
        self.time_remaining = max(0, self.time_remaining - elapsed)
        self.last_tick = current_time
        
        # Update enemies and remove dead ones
        old_enemy_count = len(self.enemies)
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
        self.kills += old_enemy_count - len(self.enemies)  # Mettre à jour le compteur de kills
        
        for enemy in self.enemies:
            enemy.tick()

    def reset(self):
        # Reset to initial state
        self.difficulty = 1
        self.time_remaining = 120 + (self.difficulty * 30)
        self.last_tick = time.time()
        self.player.pos = list(self.player_coordonnee)
        self.enemies.clear()
        self.kills = 0
        self.labyrinthe.level = self
        
        # Regénérer le labyrinthe et les ennemis
        self.labyrinthe.generer()
        self.spawn_enemies()
        self.mark_exit()

    def timer_end(self):
        if self.time_remaining <= 0:
            self.player.death()

    def win(self):
        if self.player_coordonnee == self.exit_coordonnee:
            print("win")

    def next_level(self):
        """Passe au niveau suivant avec une difficulté accrue"""
        # Générer un nouveau labyrinthe
        self.labyrinthe.generer()
        
        # Augmenter la difficulté
        self.difficulty += 1
        
        # Réinitialiser le niveau avec la nouvelle difficulté
        self.time_remaining = 120 + (self.difficulty * 30)
        self.last_tick = time.time()
        self.player.pos = list(self.player_coordonnee)
        self.enemies.clear()
        
        # Spawn de nouveaux ennemis
        self.spawn_enemies()
        
        # Marquer la nouvelle sortie
        self.mark_exit()