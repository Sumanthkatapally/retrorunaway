import pygame
import os
from constants import IMAGES_PATH

class HidingSpot(pygame.sprite.Sprite):
    def __init__(self, x, y, asset):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGES_PATH, asset)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
