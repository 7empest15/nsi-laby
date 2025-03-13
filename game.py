from render import render
from utils.event_dispatcher import dispatcher
from game_states import GameState, MenuScreen
import pygame
import time

class Game:
    def __init__(self, player, level, screen):
        self.player = player
        self.level = level
        self.screen = screen
        self.running = True
        self.state = GameState.MENU
        self.menu = MenuScreen(screen)
        self.start_time = None
        self.font = pygame.font.Font(None, 36)

    def start(self):
        while self.running:
            if self.state == GameState.MENU:
                self.menu.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    self.state = self.menu.handle_input(event)
                    if self.state == GameState.PLAYING:
                        self.start_time = time.time()
            
            elif self.state == GameState.PLAYING:
                self.tick()
                if not self.render_game():  # Si render_game renvoie False, on ferme le jeu
                    self.running = False
                    break
                
            elif self.state in [GameState.GAME_OVER, GameState.WIN]:
                self.render_end_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    self.handle_end_screen_input(event)

    def tick(self):
        self.level.tick()
        self.player.tick()
        
        # Gérer l'attaque du joueur avec la touche ESPACE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.try_attack(self.level.enemies, self.level.labyrinthe)
        
        # Vérifier la condition de victoire
        if self.player.pos == list(self.level.exit_coordonnee):
            self.state = GameState.WIN
        
        # Vérifier les conditions de défaite
        if self.player.hp <= 0 or self.level.time_remaining <= 0:
            self.state = GameState.GAME_OVER

        # Mettre à jour les monstres
        for enemy in self.level.enemies:
            enemy.labyrinthe = self.level.labyrinthe
            enemy.set_target(self.player)
            enemy.tick()

    def render_game(self):
        result = render(self.level.labyrinthe, self.screen, 20, 5, self.player, self.level.enemies)
        
        # Render timer, HP and stats
        timer_text = self.font.render(f'Time: {int(self.level.time_remaining)}s', True, (255, 255, 255))
        hp_text = self.font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
        level_text = self.font.render(f'Level: {self.level.difficulty}', True, (255, 255, 255))
        kills_text = self.font.render(f'Kills: {self.level.kills}', True, (255, 255, 255))
        
        self.screen.blit(timer_text, (10, 10))
        self.screen.blit(hp_text, (10, 50))
        self.screen.blit(level_text, (10, 90))
        self.screen.blit(kills_text, (10, 130))
        
        pygame.display.flip()
        return result

    def render_end_screen(self):
        self.screen.fill((0, 0, 0))
        if self.state == GameState.WIN:
            message = f"NIVEAU {self.level.difficulty} TERMINÉ !"
            sub_message = "Appuyez sur ESPACE pour le niveau suivant"
        else:
            message = "GAME OVER"
            sub_message = f"Score final: Niveau {self.level.difficulty}, {self.level.kills} kills"
            
        text = self.font.render(message, True, (255, 255, 255))
        sub_text = self.font.render(sub_message, True, (255, 255, 255))
        restart_text = self.font.render("Appuyez sur R pour recommencer", True, (255, 255, 255))
        
        text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30))
        sub_rect = sub_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 10))
        restart_rect = restart_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        
        self.screen.blit(text, text_rect)
        self.screen.blit(sub_text, sub_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def handle_end_screen_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_SPACE and self.state == GameState.WIN:
                self.next_level()

    def next_level(self):
        self.level.next_level()
        self.state = GameState.PLAYING
        self.start_time = time.time()

    def reset_game(self):
        # Reset player position and stats
        self.player.pos = list(self.level.player_coordonnee)
        self.player.hp = 100
        
        # Reset level
        self.level.reset()
        
        # Reset game state
        self.state = GameState.PLAYING
        self.start_time = time.time()