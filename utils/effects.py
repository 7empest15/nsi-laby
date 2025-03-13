import pygame
import time

class Effects:
    def __init__(self):
        # Charger les sons
        pygame.mixer.init()
        """ self.death_sound = pygame.mixer.Sound("assets/death.wav")
        self.hit_sound = pygame.mixer.Sound("assets/hit.wav") """
        
        # Effets visuels
        self.death_particles = []  # Liste des particules pour l'animation de mort
        
    def play_death_sound(self):
        pass
        """ self.death_sound.play() """
        
    def play_hit_sound(self):
        pass
        """ self.hit_sound.play() """
        
    def create_death_effect(self, pos, color):
        """Crée un effet de particules à la position donnée"""
        current_time = time.time() * 1000
        num_particles = 8
        
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * 3.14159
            speed = 0.1
            velocity = pygame.math.Vector2()
            velocity.from_polar((1, angle * 180 / 3.14159))
            velocity *= speed
            
            self.death_particles.append({
                'pos': list(pos),
                'vel': velocity,
                'color': color,
                'birth_time': current_time,
                'lifetime': 500  # Durée de vie en millisecondes
            })
            
    def update_and_render(self, screen, offset_x, offset_y, cell_size):
        """Met à jour et dessine les particules"""
        current_time = time.time() * 1000
        remaining_particles = []
        
        for particle in self.death_particles:
            age = current_time - particle['birth_time']
            if age < particle['lifetime']:
                # Mettre à jour la position
                particle['pos'][0] += particle['vel'].x
                particle['pos'][1] += particle['vel'].y
                
                # Calculer la position à l'écran
                screen_x = offset_x + particle['pos'][0] * cell_size + cell_size // 2
                screen_y = offset_y + particle['pos'][1] * cell_size + cell_size // 2
                
                # Calculer l'opacité (fade out)
                alpha = 255 * (1 - age / particle['lifetime'])
                color = list(particle['color'])
                color[3] = int(alpha)
                
                # Dessiner la particule
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), 3)
                remaining_particles.append(particle)
                
        self.death_particles = remaining_particles

# Instance globale pour les effets
effects = Effects() 