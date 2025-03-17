from enum import Enum
import pygame

class AbilityType(Enum):
    FAST_ATTACK = "fast_attack"
    SLOW_MOVEMENT = "slow_movement"
    EXTRA_DAMAGE = "extra_damage"
    FRAGILE = "fragile"
    SHOW_PATH = "show_path"  # Nouvelle capacité

class Abilities:
    def __init__(self, abilities=None):
        self.abilities = abilities if abilities else []

    def apply(self, player, level, screen):
        for ability in self.abilities:
            if ability == AbilityType.FAST_ATTACK:
                player.attack_cooldown = 500  # Réduire le cooldown d'attaque
            elif ability == AbilityType.SLOW_MOVEMENT:
                player.speed = max(1, player.speed - 1)  # Réduire la vitesse de déplacement
            elif ability == AbilityType.EXTRA_DAMAGE:
                player.atk += 5  # Augmenter les dégâts d'attaque
            elif ability == AbilityType.FRAGILE:
                player.hp = max(1, player.hp - 10)  # Réduire les points de vie
            elif ability == AbilityType.SHOW_PATH:
                self.show_path(player, level, screen)

    def show_path(self, player, level, screen):
        if not level.path_to_exit:
            return
        
        cell_size = 32  # Assuming each cell is 32x32 pixels
        path = level.path_to_exit
        
        for i in range(len(path) - 1):
            start_pos = (path[i][0] * cell_size + cell_size // 2, path[i][1] * cell_size + cell_size // 2)
            end_pos = (path[i + 1][0] * cell_size + cell_size // 2, path[i + 1][1] * cell_size + cell_size // 2)
            pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 5)