from enum import Enum
import pygame
from utils.event_dispatcher import dispatcher

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    WIN = 4

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.state = GameState.MENU
        self.background = pygame.image.load('assets/background.png')
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        
    def render(self):
        self.screen.blit(self.background, (0, 0))
        title = self.font.render('Labyrinthe', True, (255, 255, 255))
        start = self.font.render('Appuyez sur ESPACE', True, (255, 255, 255))
        
        title_rect = title.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//3))
        start_rect = start.get_rect(center=(self.screen.get_width()//2, 2*self.screen.get_height()//3))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(start, start_rect)
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = GameState.PLAYING
            
        return self.state