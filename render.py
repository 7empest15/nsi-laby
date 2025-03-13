import pygame
from utils.warfog import Warfog
from utils.event_dispatcher import dispatcher
from utils.effects import effects

def render(labyrinthe, screen, taille_case, espace, player, enemies):
    renderFog = False
    warfog = Warfog(50)
    largeur = labyrinthe.largeur
    hauteur = labyrinthe.hauteur

    murs = labyrinthe.get_murs()
    player_pos = list(player.pos)

    def can_move_to(new_pos):
        i, j = new_pos
        if i < 0 or i >= largeur or j < 0 or j >= hauteur:
            return False
        case = labyrinthe.laby[i][j]
        if player_pos[0] < i and case.murW:
            return False
        if player_pos[0] > i and case.murE:
            return False
        if player_pos[1] < j and case.murN:
            return False
        if player_pos[1] > j and case.murS:
            return False
            
        # Vérifier les collisions avec les monstres
        for enemy in enemies:
            if enemy.pos[0] == i and enemy.pos[1] == j:
                return False
                
        return True

    def handle_keydown(event):
        nonlocal renderFog
        new_pos = list(player_pos)
        if event.key == pygame.K_LEFT:
            new_pos[0] -= 1
        elif event.key == pygame.K_RIGHT:
            new_pos[0] += 1
        elif event.key == pygame.K_UP:
            new_pos[1] -= 1
        elif event.key == pygame.K_DOWN:
            new_pos[1] += 1
        elif event.key == pygame.K_f:
            renderFog = not renderFog
        if can_move_to(new_pos):
            player_pos[0], player_pos[1] = new_pos
            player.pos = player_pos

    dispatcher.subscribe_keydown(pygame.K_LEFT, handle_keydown)
    dispatcher.subscribe_keydown(pygame.K_RIGHT, handle_keydown)
    dispatcher.subscribe_keydown(pygame.K_UP, handle_keydown)
    dispatcher.subscribe_keydown(pygame.K_DOWN, handle_keydown)
    dispatcher.subscribe_keydown(pygame.K_f, handle_keydown)

    for event in pygame.event.get():
        dispatcher.dispatch(event)
        if event.type == pygame.QUIT:
            return False

    screen.fill((0, 0, 0))

    # Calculate the size of the visible area
    cell_size = taille_case + espace
    visible_width = screen.get_width() // cell_size
    visible_height = screen.get_height() // cell_size

    # Calculate offset to center the player
    offset_x = screen.get_width() // 2 - player_pos[0] * cell_size - cell_size // 2
    offset_y = screen.get_height() // 2 - player_pos[1] * cell_size - cell_size // 2

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

                # Définir la couleur et l'épaisseur des murs
                wall_color = (100, 100, 100)  # Gris
                line_thickness = 2

                # Dessiner les murs pour cette cellule
                if labyrinthe.laby[i][j].murN:
                    pygame.draw.line(screen, wall_color, (x, y), (x + taille_case, y), line_thickness)
                    pygame.draw.line(screen, wall_color, (x, y + line_thickness - 1), (x + taille_case, y + line_thickness - 1), line_thickness)
                if labyrinthe.laby[i][j].murS:
                    pygame.draw.line(screen, wall_color, (x, y + taille_case), (x + taille_case, y + taille_case), line_thickness)
                    pygame.draw.line(screen, wall_color, (x, y + taille_case - line_thickness + 1), (x + taille_case, y + taille_case - line_thickness + 1), line_thickness)
                if labyrinthe.laby[i][j].murW:
                    pygame.draw.line(screen, wall_color, (x, y), (x, y + taille_case), line_thickness)
                    pygame.draw.line(screen, wall_color, (x + line_thickness - 1, y), (x + line_thickness - 1, y + taille_case), line_thickness)
                if labyrinthe.laby[i][j].murE:
                    pygame.draw.line(screen, wall_color, (x + taille_case, y), (x + taille_case, y + taille_case), line_thickness)
                    pygame.draw.line(screen, wall_color, (x + taille_case - line_thickness + 1, y), (x + taille_case - line_thickness + 1, y + taille_case), line_thickness)


    # Draw player with health bar
    player_screen_x = screen.get_width() // 2
    player_screen_y = screen.get_height() // 2
    
    # Health bar background
    health_bar_width = taille_case
    health_bar_height = 5
    health_bar_y = player_screen_y - taille_case//2 - 10
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

    # Draw enemies with health bars
    for enemy in enemies:
        enemy_screen_x = offset_x + enemy.pos[0] * cell_size + cell_size // 2
        enemy_screen_y = offset_y + enemy.pos[1] * cell_size + cell_size // 2
        
        # Only draw enemies that are visible on screen
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
            enemy_color = enemy.color[:3]  # Utiliser la couleur définie dans la classe
            pygame.draw.circle(screen, enemy_color, (enemy_screen_x, enemy_screen_y), taille_case // 3)

    # Render particle effects
    effects.update_and_render(screen, offset_x, offset_y, cell_size)

    if renderFog:
        warfog.render(screen, (player_screen_x, player_screen_y))

    pygame.display.flip()
    return True