import pygame

class Warfog:
    def __init__(self, radius):
        self.radius = radius

    def render(self, screen, center):
        width, height = screen.get_size()
        fog_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        fog_surface.fill((0, 0, 0, 255))  # Fill with semi-transparent black

        # Draw a transparent circle around the player
        pygame.draw.circle(fog_surface, (0, 0, 0, 0), center, self.radius)

        screen.blit(fog_surface, (0, 0))