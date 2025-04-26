# Define screen width
import pygame


SCREEN_WIDTH = 800  # Example value, adjust as needed

# Camera class
class Camera:
    def __init__(self):
        self.offset = pygame.math.Vector2(0, 0)

    def update(self, player):
        # Horizontal follow (centered)
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.x = target_x
        self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH)) # Changed level_width for screen_width

    def set_level_width(self, level_width):
        self.level_width = level_width

#Game Class:
class Game:
    def __init__(self):
        #Existing Code
        self.camera = Camera()
        self.camera.set_level_width(SCREEN_WIDTH * 2)
