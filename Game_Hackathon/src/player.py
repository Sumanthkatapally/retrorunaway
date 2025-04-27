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
        self.rect  = self.image.get_rect(topleft=(x, y))

        # Physics & state
        self.velocity_y   = 0
        self.jumping      = False
        self.crouching    = False
        self.direction    = "right"
        self.outfit       = set()
        self.disco_active = False
        self.disco_time   = 0
        self.disco_count  = 0

        self.mask            = pygame.mask.from_surface(self.image)
        self.animation_speed = 0.15
        self.current_time    = 0

    def load_sprites(self):
        """Safe sprite loading with fallbacks"""
        base_image = self._load_image("Ideal_Character_State.png")
        base_image = pygame.transform.scale(base_image, (100, 150))

        self.images = {
            "idle":   [base_image],
            "run":    [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "jump":   [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "crouch": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "dance":  self._load_dance_sprites(base_image),
        }

    def load_overlays(self):
        """
        Load overlay images for each collectible piece with specific sizes and offsets.
        """
        # Per-piece display config: width×height and (dx, dy) offsets relative to base sprite
        piece_config = {
            "Bell-Bottom": {"size": (80, 80),  "offset": (10,  70)},   # pants
            "Shoe":        {"size": (60, 40),  "offset": (20, 110)},   # shoes
            "Disco-Shirt": {"size": (80, 60),  "offset": (10,  50)},   # shirt
            "Sunglasses":  {"size": (50, 20),  "offset": (25,  30)},   # glasses
            # Hair now 100×50, lifted up by 35px
            "hair":        {"size": (100, 50), "offset": (0,  -35)},   # hair
        }

        for piece in OUTFIT_ORDER:
            filename = f"{piece}.png"
            img = self._load_image(filename)
            cfg = piece_config.get(piece, {"size": (100, 80), "offset": (0, 0)})
            if img:
                overlay = pygame.transform.scale(img, cfg["size"])
            else:
                overlay = pygame.Surface(cfg["size"], pygame.SRCALPHA)
            self.overlays[piece] = (overlay, cfg["offset"])

    def _load_image(self, filename, fallback=None):
        """Safe image loader with error fallback"""
        try:
            path = os.path.join(IMAGES_PATH, filename)
            img = pygame.image.load(path).convert_alpha()
            if fallback is None:
                img = pygame.transform.scale(img, (100, 150))
            return img
        except (FileNotFoundError, pygame.error):
            return fallback or pygame.Surface((100, 150), pygame.SRCALPHA)

    def _load_dance_sprites(self, fallback):
        """Use available progression sprites for disco animation"""
        return [
            self._load_image("Character-after-collecting-Bell-Bottom.png",                                             fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-and-Disco-shirt.png",                              fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-Disco-Shirt-and-Sunglasses.png",                    fallback),
            self._load_image("Character-after-collecting-Bell-Bottom-Disco-Shirt-Sunglasses-shoes-and-hair.png",        fallback),
        ]

    def update(self, platforms=None):
        """Movement, gravity, and disco-frame cycling."""
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y     += self.velocity_y

        # Platform collision
        if platforms:
            self._handle_platform_collision(platforms)

        # Disco animation cycle
        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            if self.disco_active and self.images["dance"]:
                self.current_sprite = (self.current_sprite + 1) % len(self.images["dance"])
                self.image = self.images["dance"][self.current_sprite]

    def _handle_platform_collision(self, platforms):
        """Stop vertical movement and reset jumping when landing."""
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.velocity_y  = 0
            self.jumping      = False

    def add_outfit_piece(self, piece):
        """Collect a piece; disco logic stays the same."""
        self.outfit.add(piece)
        if piece == "Disco-Shirt":
            self.disco_count += 1
            if self.disco_count >= 3:
                self.activate_disco()

    def activate_disco(self):
        self.disco_active = True
        self.disco_time   = pygame.time.get_ticks()

    def jump(self):
        """Apply jump impulse if not already jumping."""
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping    = True

    def crouch(self, toggle):
        self.crouching = toggle

    def draw(self, surface, camera):
        """Draw the base sprite, then layer on each collected overlay."""
        x = self.rect.x - camera.offset.x
        y = self.rect.y - camera.offset.y

        # Base character (always 100×150)
        surface.blit(self.image, (x, y))

        # Overlays in outfit order
        for piece in OUTFIT_ORDER:
            if piece in self.outfit:
                overlay, (dx, dy) = self.overlays[piece]
                surface.blit(overlay, (x + dx, y + dy))
