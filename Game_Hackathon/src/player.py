import pygame
import os
from constants import IMAGES_PATH, GRAVITY, JUMP_STRENGTH

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {}
        self.current_sprite = 0
        self.load_sprites()
        self.image = self.images["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jumping = False
        self.crouching = False
        self.direction = "right"
        self.outfit = set()
        self.disco_active = False
        self.disco_time = 0
        self.disco_count = 0
        self.mask = pygame.mask.from_surface(self.images["idle"][0])
        self.animation_speed = 0.15
        self.current_time = 0

    def load_sprites(self):
        """Safe sprite loading with fallbacks"""
        base_image = self._load_image("Ideal_Character_State.png")
        base_image = pygame.transform.scale(base_image, (100, 150))  # Scale base image

        # Core sprites
        self.images = {
            "idle": [base_image],
            "run": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "jump": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "crouch": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "dance": self._load_dance_sprites(base_image),
        }

    def _load_image(self, filename, fallback=None):
        """Safe image loader with error fallback"""
        try:
            image = pygame.image.load(os.path.join(IMAGES_PATH, filename)).convert_alpha()
            if fallback is None:
                image = pygame.transform.scale(image, (100, 150))  # Scale image
            return image
        except (FileNotFoundError, pygame.error) as e:
            print(f"Missing image: {filename} - {str(e)}")
            return fallback or pygame.Surface((50, 100), pygame.SRCALPHA)

    def _load_dance_sprites(self, fallback):
        """Use available progression sprites"""
        return [
            self._load_image("Character-after-collecting-Bell-Bottom.png", fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-and-Disco-shirt.png", fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-Disco-Shirt-and-Sunglasses.png", fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-Disco-Shirt-Sunglasses-shoes-and-hair.png", fallback)
        ]

    def update(self, platforms=None):
        """Movement and animation logic"""
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Platform collision
        if platforms:
            self._handle_platform_collision(platforms)

        # Animation updates
        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            if self.disco_active and len(self.images["dance"]) > 0:
                self.current_sprite = (self.current_sprite + 1) % len(self.images["dance"])
                self.image = self.images["dance"][self.current_sprite]

    def _handle_platform_collision(self, platforms):
        """Check for platform landings"""
        self.rect.y += 1  # Small downward movement
        platform_hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1  # Reset position

        if platform_hits:
            self.rect.bottom = platform_hits[0].rect.top
            self.velocity_y = 0
            self.jumping = False

    def add_outfit_piece(self, piece):
        """Handle outfit progression"""
        self.outfit.add(piece)
        if "Disco-Shirt" in self.outfit:
            self.disco_count += 1
            if self.disco_count >= 3:
                self.activate_disco()

    def activate_disco(self):
        """Enable disco mode effects"""
        self.disco_active = True
        self.disco_time = pygame.time.get_ticks()

    def draw(self, surface, camera):
        """Draw with camera offset"""
        surface.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True

    def crouch(self, toggle):
        self.crouching = toggle
