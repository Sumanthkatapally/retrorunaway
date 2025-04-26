import pygame
import os
from constants import IMAGES_PATH, TILE_SIZE

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = pygame.image.load(os.path.join(IMAGES_PATH, f"{item_type}.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # scale it
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False

    def draw(self, screen, camera):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
