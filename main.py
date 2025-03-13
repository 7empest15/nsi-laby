from labyrinth.labyrinth import Labyrinthe
from entities.player import Player
from levels.level import Level
from entities.monster import Monster, Caecior
from game import Game
from utils.event_dispatcher import dispatcher
import pygame

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Labyrinthe')

    # Create the labyrinth
    labyrinthe = Labyrinthe(20, 20)
    labyrinthe.generer()

    # Create the player at starting position with better stats
    player = Player(100, 0, 1, 20, 5, 1, (0, 0))  # Increased player damage

    # Create the level with exit at bottom-right corner
    level = Level(labyrinthe, player, (19, 19), (0, 0))
    
    # Add different types of monsters with very balanced stats
    # Normal monsters: Low HP, low damage, fast attack
    level.spawn_enemy(Monster, 30, 1, 10, 1, 1)  # HP=30, damage=10, speed=1
    level.spawn_enemy(Monster, 30, 1, 10, 1, 1)
    
    # Caecior: Higher HP, medium damage, slower attack, fog ability
    level.spawn_enemy(Caecior, 40, 1, 15, 1, 1)  # HP=40, damage=15, speed=1
    
    # Create and start the game
    game = Game(player, level, screen)  
    game.start()

    # Cleanup
    pygame.quit()

if __name__ == '__main__':
    main()