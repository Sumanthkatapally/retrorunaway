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
        base_image = pygame.transform.scale(base_image, (100, 150))  # Scale base image

        # Core sprites
        self.images = {
            "idle": [base_image],
            "run": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "jump": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "crouch": [self._load_image("Character-after-collecting-Bell-Bottom.png", base_image)],
            "dance": self._load_dance_sprites(base_image),
        }

    def load_overlays(self):
        """
        Load separate overlay images for each collectible piece.
        These will be blitted on top of the base sprite when collected.
        """
        for piece in OUTFIT_ORDER:
            filename = f"{piece}.png"
            image = self._load_image(filename)
            if image:
                overlay = pygame.transform.scale(image, (100, 150))
            else:
                # Transparent surface if missing
                overlay = pygame.Surface((100, 150), pygame.SRCALPHA)
            self.overlays[piece] = overlay

    def _load_image(self, filename, fallback=None):
        """Safe image loader with error fallback"""
        try:
            path = os.path.join(IMAGES_PATH, filename)
            image = pygame.image.load(path).convert_alpha()
            # If no fallback, scale to default
            if fallback is None:
                image = pygame.transform.scale(image, (100, 150))
            return image
        except (FileNotFoundError, pygame.error) as e:
            print(f"Missing image: {filename} - {e}")
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
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Platform collision
        if platforms:
            self._handle_platform_collision(platforms)

        # Animation updates (only disco cycles)
        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            if self.disco_active and len(self.images["dance"]) > 0:
                self.current_sprite = (self.current_sprite + 1) % len(self.images["dance"])
                self.image = self.images["dance"][self.current_sprite]

    def _handle_platform_collision(self, platforms):
        """Check for platform landings"""
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 1

        if hits:
            self.rect.bottom = hits[0].rect.top
            self.velocity_y = 0
            self.jumping = False

    def add_outfit_piece(self, piece):
        """Handle outfit progression and update overlays"""
        self.outfit.add(piece)
        # Overlays handle costume display
        # Track for disco activation
        if "Disco-Shirt" in self.outfit:
            self.disco_count += 1
            if self.disco_count >= 3:
                self.activate_disco()

    def activate_disco(self):
        """Enable disco mode effects"""
        self.disco_active = True
        self.disco_time = pygame.time.get_ticks()

    def draw(self, surface, camera):
        """Draw the base sprite and any collected overlays"""
        x = self.rect.x - camera.offset.x
        y = self.rect.y - camera.offset.y
        # Base image (idle or disco)
        surface.blit(self.image, (x, y))
        # Draw overlays in defined order
        for piece in OUTFIT_ORDER:
            if piece in self.outfit:
                surface.blit(self.overlays[piece], (x, y))

    def jump(self):
        if not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True

    def crouch(self, toggle):
        self.crouching = toggle

    # Note: '_update_outfit_sprite' is no longer needed, overlays handle display
