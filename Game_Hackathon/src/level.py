# File: src/level.py
import pygame
import random
import os
from bouncer import Bouncer
from collectible import Collectible
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    TILE_SIZE, IMAGES_PATH
)

class HidingSpot(pygame.sprite.Sprite):
    def __init__(self, x, y, asset):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGES_PATH, asset)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

class Level:
    def __init__(self, level_data):
        self.name         = level_data["name"]
        self.bg_color     = level_data["bg_color"]
        self.music        = level_data["music"]
        self.enemies      = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.platforms    = pygame.sprite.Group()
        self.hiding_spots = pygame.sprite.Group()
        self.setup_level(level_data)

    def setup_level(self, level_data):
        # 1) Platforms
        for x in range(0, SCREEN_WIDTH*2, TILE_SIZE):
            self.platforms.add(Platform(x, SCREEN_HEIGHT-50, TILE_SIZE, 50))

        # 2) Hiding spots (cars vs chains)
        # Decide asset list and y-position based on flag or name
        use_cars = level_data.get('hiding_spots') == 'cars' or 'Parking' in self.name
        asset_list = ["car1.png", "car2.png", "car3.png"] if use_cars else ["Chain.png"]
        y_pos = SCREEN_HEIGHT - 150 if use_cars else SCREEN_HEIGHT - 120

        for _ in range(3):
            x = random.randint(100, SCREEN_WIDTH-100)
            asset = random.choice(asset_list)
            self.hiding_spots.add(HidingSpot(x, y_pos, asset))

        # 3) Enemies (bouncers)
        for _ in range(level_data["enemies"]):
            placed, attempts = False, 0
            while not placed and attempts < 20:
                x = random.randint(100, SCREEN_WIDTH-100)
                y = SCREEN_HEIGHT - TILE_SIZE - 50
                patrol_y = y
                pts = [
                    (random.randint(0, SCREEN_WIDTH), patrol_y),
                    (random.randint(SCREEN_WIDTH, SCREEN_WIDTH*2), patrol_y)
                ]
                b = Bouncer(x, y, pts)
                if not any(pygame.sprite.collide_rect(b, p) for p in self.platforms):
                    self.enemies.add(b)
                    placed = True
                attempts += 1
            if not placed:
                print("Warning: Could not place bouncer.")

        # 4) Collectibles
        for it in level_data["collectibles"]:
            placed, attempts = False, 0
            while not placed and attempts < 10:
                x = random.randint(100, SCREEN_WIDTH*2-100)
                y = SCREEN_HEIGHT - 250
                c = Collectible(x, y, it)
                if not any(pygame.sprite.collide_rect(c, p) for p in self.platforms) and \
                   not any(pygame.sprite.collide_rect(c, h) for h in self.hiding_spots):
                    self.collectibles.add(c)
                    placed = True
                attempts += 1
            if not placed:
                print(f"Warning: Could not place {it}.")

        # 5) Disco ball (optional)
        if random.random() > 0.5:
            x = random.randint(100, SCREEN_WIDTH*2-100)
            self.collectibles.add(Collectible(x, SCREEN_HEIGHT-200, "Disco-Ball"))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((50,50,50))
        pygame.draw.rect(self.image, (100,100,100), (0,0,w,h), 3)
        self.rect = self.image.get_rect(topleft=(x,y))
