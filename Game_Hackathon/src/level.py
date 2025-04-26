import pygame
import random
import os
from bouncer import Bouncer
from collectible import Collectible
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TILE_SIZE,
    IMAGES_PATH,
    OUTFIT_ORDER,
    BLACK,
)

class HidingSpot(pygame.sprite.Sprite): # Create the hiding_spot class.
    def __init__(self, x, y, asset):
        super().__init__()
        self.image = pygame.image.load(os.path.join(IMAGES_PATH, asset)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Level:
    def __init__(self, level_data):
        self.name = level_data["name"]
        self.bg_color = level_data["bg_color"]
        self.music = level_data["music"]
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.hiding_spots = pygame.sprite.Group()
        self.setup_level(level_data)

    def setup_level(self, level_data):
        # Create platforms
        for x in range(0, SCREEN_WIDTH * 2, TILE_SIZE):  # Spanning the entire level
            self.platforms.add(Platform(x, SCREEN_HEIGHT - 50, TILE_SIZE, 50))

        # Create hiding spots (cars/dumpsters)
        for i in range(3):
            x = random.randint(100, SCREEN_WIDTH - 100)  # Keep within screen width
            if "Parking" in self.name:
                car_type = random.choice(["car1.png", "car2.png", "car3.png"])
                self.hiding_spots.add(HidingSpot(x, SCREEN_HEIGHT - 150, car_type))
            else:
                self.hiding_spots.add(HidingSpot(x, SCREEN_HEIGHT - 120, "Chain.png"))

        # Create enemies
        for i in range(level_data["enemies"]):
            placed = False
            attempts = 0
            while not placed and attempts < 20:  # Changed to 20
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = SCREEN_HEIGHT - 100
                patrol_points = [
                    (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 100),
                    (
                        random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2),
                        SCREEN_HEIGHT - 100,
                    ),
                ]
                bouncer = Bouncer(x, y, patrol_points)
                colliding = False
                for sprite in self.platforms:
                    if pygame.sprite.collide_rect(bouncer, sprite):
                        colliding = True
                        break
                if not colliding:
                    self.enemies.add(bouncer)
                    placed = True
                attempts += 1
            if not placed:
                print(f"Warning: Could not place bouncer after several attempts.")

        # Create collectibles
        for item_type in level_data["collectibles"]:
            placed = False
            attempts = 0
            while not placed and attempts < 10:
                x = random.randint(100, SCREEN_WIDTH * 2 - 100)
                y = SCREEN_HEIGHT - 250
                collectible = Collectible(x, y, item_type)
                colliding = False
                for sprite in self.platforms:
                    if pygame.sprite.collide_rect(collectible, sprite):
                        colliding = True
                        break
                for sprite in self.hiding_spots:
                    if pygame.sprite.collide_rect(collectible, sprite):
                        colliding = True
                        break
                if not colliding:
                    self.collectibles.add(collectible)
                    placed = True
                attempts += 1
            if not placed:
                print(
                    f"Warning: Could not place collectible {item_type} after several attempts."
                )

        # Add disco ball
        if random.random() > 0.5:
            x = random.randint(100, SCREEN_WIDTH * 2 - 100)
            self.collectibles.add(Collectible(x, SCREEN_HEIGHT - 200, "Disco-Ball"))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((50, 50, 50))
        pygame.draw.rect(self.image, (100, 100, 100), (0, 0, width, height), 3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
