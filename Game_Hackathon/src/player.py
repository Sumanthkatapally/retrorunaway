import pygame
import os
from constants import IMAGES_PATH, GRAVITY, JUMP_STRENGTH, OUTFIT_ORDER

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {}
        self.overlays = {}
        self.current_sprite = 0
        self.load_sprites()
        self.load_overlays()

        # Initial display image is the base idle sprite
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
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_speed = 0.15
        self.current_time = 0

    def load_sprites(self):
        """Safe sprite loading with fallbacks"""
        base_image = self._load_image("Ideal_Character_State.png")
        base_image = pygame.transform.scale(base_image, (100, 150))

        self.images = {
            "idle": [base_image],
            "run": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "jump": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "crouch": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "dance": self._load_dance_sprites(base_image),
        }

    def load_overlays(self):
        """
        Load overlay images for each collectible piece with specific sizes and offsets.
        """
        # Define per-piece display config: size and (dx, dy) offsets
        piece_config = {
            # Pants overlay: half-height, centered on lower body
            "Bell-Bottom": {"size": (80, 80), "offset": (10, 70)},
            # Shoes overlay: sits at feet
            "Shoe":         {"size": (60, 40), "offset": (20, 110)},
            # Shirt overlay: upper body area
            "Disco-Shirt":  {"size": (80, 60), "offset": (10, 50)},
            # Sunglasses overlay: around face
            "Sunglasses":   {"size": (50, 20), "offset": (25, 30)},
            # Hair overlay: above head
            "hair":         {"size": (70, 40), "offset": (15, -10)},
        }
        for piece in OUTFIT_ORDER:
            filename = f"{piece}.png"
            img = self._load_image(filename)
            config = piece_config.get(piece, {"size": (100, 80), "offset": (0, 0)})
            if img:
                overlay = pygame.transform.scale(img, config["size"])
            else:
                overlay = pygame.Surface(config["size"], pygame.SRCALPHA)
            self.overlays[piece] = (overlay, config["offset"])

    def _load_image(self, filename, fallback=None):
        """Safe image loader with error fallback"""
        try:
            path = os.path.join(IMAGES_PATH, filename)
            image = pygame.image.load(path).convert_alpha()
            if fallback is None:
                image = pygame.transform.scale(image, (100, 150))
            return image
        except (FileNotFoundError, pygame.error):
            return fallback or pygame.Surface((100, 150), pygame.SRCALPHA)

    def _load_dance_sprites(self, fallback):
        """Use available progression sprites for disco animation"""
        return [
            self._load_image("Character-after-collecting-Bell-Bottom.png", fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-and-Disco-shirt.png", fallback),
            self._load_image(
                "Character-after-collecting-Bell-Bottom-Disco-Shirt-and-Sunglasses.png", fallback
            ),
            self._load_image(
                "Character-after-collecting-Bell-Bottom-Disco-Shirt-Sunglasses-shoes-and-hair.png",
                fallback,
            ),
        ]

    def update(self, platforms=None):
        """Movement and animation logic"""
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if platforms:
            self._handle_platform_collision(platforms)

        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            if self.disco_active and self.images["dance"]:
                self.current_sprite = (self.current_sprite + 1) % len(self.images["dance"])
                self.image = self.images["dance"][self.current_sprite]

    def _handle_platform_collision(self, platforms):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.velocity_y = 0
            self.jumping = False

    def add_outfit_piece(self, piece):
        """Handle outfit progression and overlay display"""
        self.outfit.add(piece)
        if "Disco-Shirt" in self.outfit:
            self.disco_count += 1
            if self.disco_count >= 3:
                self.activate_disco()

    def activate_disco(self):
        self.disco_active = True
        self.disco_time = pygame.time.get_ticks()

    def draw(self, surface, camera):
        """Draw base sprite then overlays in correct positions"""
        x = self.rect.x - camera.offset.x
        y = self.rect.y - camera.offset.y
        surface.blit(self.image, (x, y))
        for piece in OUTFIT_ORDER:
            if piece in self.outfit:
                overlay, (dx, dy) = self.overlays[piece]
                surface.blit(overlay, (x + dx, y + dy))

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True

    def crouch(self, toggle):
        self.crouching = toggle
