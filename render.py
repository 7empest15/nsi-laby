import pygame
from utils.warfog import Warfog
from utils.event_dispatcher import dispatcher
from utils.effects import effects
from abilities.abilities import AbilityType
from entities.monster import Caecior

def render(labyrinthe, screen, taille_case, espace, player, enemies, medkits):
    renderFog = False
    warfog = Warfog(50)
    largeur = labyrinthe.largeur
    hauteur = labyrinthe.hauteur
    
    # Constantes pour l'interface utilisateur
    UI_MARGIN = 10
    UI_LINE_HEIGHT = 40
    UI_FONT_SIZE = 36
    font = pygame.font.Font(None, UI_FONT_SIZE)
    
    # Constantes pour le mouvement
    MOVEMENT_DELAY = 100  # Délai entre les mouvements en millisecondes
    last_move_time = 0

    def can_move_to(new_pos):
        i, j = new_pos
        current_i, current_j = player.pos
        
        # Vérifier les limites du labyrinthe
        if i < 0 or i >= largeur or j < 0 or j >= hauteur:
            return False
            
        # Un seul déplacement à la fois (pas de diagonale)
        if abs(i - current_i) + abs(j - current_j) != 1:
            return False
            
        # Vérifier les murs
        current_case = labyrinthe.laby[current_i][current_j]
        destination_case = labyrinthe.laby[i][j]
        
        # Déplacement horizontal
        if i > current_i:  # Droite
            if current_case.murE or destination_case.murW:
                return False
        elif i < current_i:  # Gauche
            if current_case.murW or destination_case.murE:
                return False
        # Déplacement vertical
        elif j > current_j:  # Bas
            if current_case.murS or destination_case.murN:
                return False
        elif j < current_j:  # Haut
            if current_case.murN or destination_case.murS:
                return False
            
        # Vérifier les collisions avec les monstres
        for enemy in enemies:
            if enemy.pos[0] == i and enemy.pos[1] == j:
                return False
                
        return True

    # Traiter tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                renderFog = not renderFog
            else:
                new_pos = list(player.pos)
                if event.key == pygame.K_q:
                    new_pos[0] -= 1
                elif event.key == pygame.K_d:
                    new_pos[0] += 1
                elif event.key == pygame.K_z:
                    new_pos[1] -= 1
                elif event.key == pygame.K_s:
                    new_pos[1] += 1
                
                if can_move_to(new_pos):
                    player.pos = new_pos

    screen.fill((0, 0, 0))

    # Calculate the size of the visible area
    cell_size = taille_case + espace
    visible_width = screen.get_width() // cell_size
    visible_height = screen.get_height() // cell_size

    # Calculate offset to center the player
    offset_x = screen.get_width() // 2 - player.pos[0] * cell_size - cell_size // 2
    offset_y = screen.get_height() // 2 - player.pos[1] * cell_size - cell_size // 2

    # Draw cells and walls
    for i in range(largeur):
        for j in range(hauteur):
            x = i * cell_size + offset_x
            y = j * cell_size + offset_y
            
            # Only draw cells that are visible on screen
            if -cell_size <= x <= screen.get_width() and -cell_size <= y <= screen.get_height():
                # Only mark exit with a subtle indicator
                if hasattr(labyrinthe.laby[i][j], 'is_exit') and labyrinthe.laby[i][j].is_exit:
                    exit_rect = pygame.Rect(x + taille_case//4, y + taille_case//4, 
                                         taille_case//2, taille_case//2)
                    pygame.draw.rect(screen, (0, 100, 0), exit_rect)  # Darker green for exit

                # Draw walls
                if labyrinthe.laby[i][j].murN:
                    pygame.draw.line(screen, (100, 100, 100), (x, y), (x + taille_case, y), 2)
                if labyrinthe.laby[i][j].murS:
                    pygame.draw.line(screen, (100, 100, 100), (x, y + taille_case), (x + taille_case, y + taille_case), 2)
                if labyrinthe.laby[i][j].murW:
                    pygame.draw.line(screen, (100, 100, 100), (x, y), (x, y + taille_case), 2)
                if labyrinthe.laby[i][j].murE:
                    pygame.draw.line(screen, (100, 100, 100), (x + taille_case, y), (x + taille_case, y + taille_case), 2)

    # Draw path to exit
    if AbilityType.SHOW_PATH in player.abilities.abilities:
        path = labyrinthe.level.path_to_exit
        if path:
            for i in range(len(path) - 1):
                start_pos = (path[i][0] * cell_size + cell_size // 2 + offset_x, path[i][1] * cell_size + cell_size // 2 + offset_y)
                end_pos = (path[i + 1][0] * cell_size + cell_size // 2 + offset_x, path[i + 1][1] * cell_size + cell_size // 2 + offset_y)
                pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 5)

    # Draw player
    player_screen_x = screen.get_width() // 2
    player_screen_y = screen.get_height() // 2
    
    # Player health bar
    health_bar_width = taille_case
    health_bar_height = 5
    health_bar_y = player_screen_y - taille_case//2 - 10
    
    # Health bar background
    pygame.draw.rect(screen, (255, 0, 0), 
                    (player_screen_x - health_bar_width//2, health_bar_y, 
                     health_bar_width, health_bar_height))
    
    # Health bar fill
    health_percentage = player.hp / 100
    pygame.draw.rect(screen, (0, 255, 0),
                    (player_screen_x - health_bar_width//2, health_bar_y,
                     health_bar_width * health_percentage, health_bar_height))
    
    # Player circle
    pygame.draw.circle(screen, (0, 0, 255), (player_screen_x, player_screen_y), taille_case // 3)

    # Draw enemies
    for enemy in enemies:
        enemy_screen_x = offset_x + enemy.pos[0] * cell_size + cell_size // 2
        enemy_screen_y = offset_y + enemy.pos[1] * cell_size + cell_size // 2
        if -taille_case <= enemy_screen_x <= screen.get_width() + taille_case and \
           -taille_case <= enemy_screen_y <= screen.get_height() + taille_case:
            # Enemy health bar
            enemy_health_percentage = enemy.hp / 100
            pygame.draw.rect(screen, (255, 0, 0),
                            (enemy_screen_x - health_bar_width//2, 
                             enemy_screen_y - taille_case//2 - 10,
                             health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0),
                            (enemy_screen_x - health_bar_width//2,
                             enemy_screen_y - taille_case//2 - 10,
                             health_bar_width * enemy_health_percentage, health_bar_height))
            
            # Enemy circle
            pygame.draw.circle(screen, enemy.color[:3], (enemy_screen_x, enemy_screen_y), taille_case // 3)


    for medkit in medkits:
        medkit_screen_x = offset_x + medkit.pos[0] * cell_size + cell_size // 2
        medkit_screen_y = offset_y + medkit.pos[1] * cell_size + cell_size // 2
        if -taille_case <= medkit_screen_x <= screen.get_width() + taille_case and \
           -taille_case <= medkit_screen_y <= screen.get_height() + taille_case:
            
            color = pygame.Color(0, 180, 0, 255)

            pygame.draw.circle(screen, color, (medkit_screen_x, medkit_screen_y), taille_case // 3)

    # Draw UI in fixed positions
    # Background for UI
    ui_background = pygame.Surface((200, 4 * UI_LINE_HEIGHT))
    ui_background.fill((0, 0, 0))
    ui_background.set_alpha(200)
    screen.blit(ui_background, (UI_MARGIN, UI_MARGIN))

    # Render UI text
    timer_text = font.render(f'Time: {int(labyrinthe.level.time_remaining)}s', True, (255, 255, 255))
    hp_text = font.render(f'HP: {player.hp}', True, (255, 255, 255))
    level_text = font.render(f'Level: {labyrinthe.level.difficulty}', True, (255, 255, 255))
    kills_text = font.render(f'Kills: {labyrinthe.level.kills}', True, (255, 255, 255))

    # Draw UI text at fixed positions
    screen.blit(timer_text, (UI_MARGIN, UI_MARGIN))
    screen.blit(hp_text, (UI_MARGIN, UI_MARGIN + UI_LINE_HEIGHT))
    screen.blit(level_text, (UI_MARGIN, UI_MARGIN + 2 * UI_LINE_HEIGHT))
    screen.blit(kills_text, (UI_MARGIN, UI_MARGIN + 3 * UI_LINE_HEIGHT))

    # Render warfog if active
    for enemy in enemies:
        if isinstance(enemy, Caecior) and enemy.fog_active:
            warfog.render(screen, (player_screen_x, player_screen_y))
            break

    if renderFog:
        warfog.render(screen, (player_screen_x, player_screen_y))

    pygame.display.flip()
    return True