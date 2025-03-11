import pygame
from labyrinthe import Labyrinthe
from warfog import Warfog


def render(labyrinthe, taille_case, espace):
    renderFog = False
    pygame.init()
    warfog = Warfog(50)
    largeur = labyrinthe.largeur
    hauteur = labyrinthe.hauteur
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Labyrinthe avec sortie')
    murs = labyrinthe.get_murs()
    
    won = False
    
    image = pygame.image.load("temp_menu.png").convert_alpha()
    scale_factor = 10
    image = pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor))
    
    # Obtenir les informations sur la sortie
    sortie_pos, sortie_dir = labyrinthe.get_sortie()
    
    player_pos = [largeur // 2, hauteur // 2]
    
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
        return True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = list(player_pos)
                if event.key == pygame.K_q:
                    new_pos[0] -= 1
                elif event.key == pygame.K_d:
                    new_pos[0] += 1
                elif event.key == pygame.K_z:
                    new_pos[1] -= 1
                elif event.key == pygame.K_s:
                    new_pos[1] += 1
                elif event.key == pygame.K_f:
                    renderFog = not renderFog
                if can_move_to(new_pos):
                    player_pos = new_pos
                    
                    # Vérifier si le joueur a atteint la sortie
                    if player_pos[0] == sortie_pos[0] and player_pos[1] == sortie_pos[1]:
                        print("Félicitations ! Vous avez trouvé la sortie !")
                        won = True
                        # Option: Réinitialiser le labyrinthe ou quitter
                        # running = False

        screen.fill((0, 0, 0))
        
        # Ajuster les offsets pour centrer le joueur dans la cellule plutôt que sur les murs
        offset_x = screen_width // 2 - (player_pos[0] * (taille_case + espace) + taille_case // 2)
        offset_y = screen_height // 2 - (player_pos[1] * (taille_case + espace) + taille_case // 2)

        # Dessiner les cases du labyrinthe
        for i in range(labyrinthe.largeur):
            for j in range(labyrinthe.hauteur):
                x = i * (taille_case + espace) + offset_x
                y = j * (taille_case + espace) + offset_y
                
                # Dessiner un indicateur visuel pour la sortie
                if sortie_pos and i == sortie_pos[0] and j == sortie_pos[1]:
                    # Remplir la case de sortie en vert
                    pygame.draw.rect(screen, (0, 255, 0), (x, y, taille_case, taille_case))
                    
                    # Dessiner une flèche ou un indicateur de direction
                    arrow_color = (255, 255, 0)  # Jaune pour plus de visibilité
                    arrow_width = 3
                    center_x = x + taille_case // 2
                    center_y = y + taille_case // 2
                    
                    if sortie_dir == 'N':
                        pygame.draw.line(screen, arrow_color, (center_x, y + taille_case // 4), (center_x, y), arrow_width)
                        pygame.draw.polygon(screen, arrow_color, [(center_x - 5, y + 5), (center_x, y), (center_x + 5, y + 5)])
                    elif sortie_dir == 'S':
                        pygame.draw.line(screen, arrow_color, (center_x, center_y), (center_x, y + taille_case), arrow_width)
                        pygame.draw.polygon(screen, arrow_color, [(center_x - 5, y + taille_case - 5), (center_x, y + taille_case), (center_x + 5, y + taille_case - 5)])
                    elif sortie_dir == 'W':
                        pygame.draw.line(screen, arrow_color, (center_x, center_y), (x, center_y), arrow_width)
                        pygame.draw.polygon(screen, arrow_color, [(x + 5, center_y - 5), (x, center_y), (x + 5, center_y + 5)])
                    elif sortie_dir == 'E':
                        pygame.draw.line(screen, arrow_color, (center_x, center_y), (x + taille_case, center_y), arrow_width)
                        pygame.draw.polygon(screen, arrow_color, [(x + taille_case - 5, center_y - 5), (x + taille_case, center_y), (x + taille_case - 5, center_y + 5)])

        # Dessiner les murs
        for mur in murs:
            (i, j), murN, murS, murW, murE = mur
            x = i * (taille_case + espace) + offset_x
            y = j * (taille_case + espace) + offset_y
            if murN:
                pygame.draw.line(screen, (255, 255, 255), (x, y), (x + taille_case, y))
            if murS:
                pygame.draw.line(screen, (255, 255, 255), (x, y + taille_case), (x + taille_case, y + taille_case))
            if murW:
                pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y + taille_case))
            if murE:
                pygame.draw.line(screen, (255, 255, 255), (x + taille_case, y), (x + taille_case, y + taille_case))

        # Dessiner le joueur au centre de la cellule plutôt que potentiellement sur un mur
        player_screen_x = screen_width // 2
        player_screen_y = screen_height // 2
        pygame.draw.circle(screen, (255, 0, 0), (player_screen_x, player_screen_y), taille_case // 3)

        if renderFog:
            warfog.render(screen, (player_screen_x, player_screen_y))

        if won:
            screen.blit(image, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    labyrinthe = Labyrinthe(20, 20)
    labyrinthe.generer()
    sortie, direction = labyrinthe.generer_sortie()
    print(f"Sortie créée en position {sortie} dans la direction {direction}")
    render(labyrinthe, 20, 5)
