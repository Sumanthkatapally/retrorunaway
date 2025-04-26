import pygame
import os
import math
import random
from constants import *

class Bouncer(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_points):
        super().__init__()
        self.patrol_points = patrol_points
        self.current_point = 0
        self.speed = BOUNCER_SPEED
        self.direction = 1
        self.alerted = False
        self.alert_timer = 0
        self.load_images()
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        self.idle_image = pygame.image.load(os.path.join(IMAGES_PATH, "Bouncer-ideal.png")).convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, (TILE_SIZE, TILE_SIZE)) # Scale it
        self.alert_image = pygame.image.load(os.path.join(IMAGES_PATH, "Bouncer-Caught-character.png")).convert_alpha()
        self.alert_image = pygame.transform.scale(self.alert_image, (TILE_SIZE, TILE_SIZE)) # Scale it

    def update(self):
        # Patrol logic
        target = self.patrol_points[self.current_point]
        if abs(self.rect.x - target[0]) < self.speed:
            self.current_point = (self.current_point + 1) % len(self.patrol_points)
            self.direction = 1 if self.patrol_points[self.current_point][0] > self.rect.x else -1
        
        self.rect.x += self.speed * self.direction
        
        # Alert state
        if self.alerted:
            self.alert_timer -= 1
            if self.alert_timer <= 0:
                self.alerted = False
                self.image = self.idle_image

    def check_vision(self, player):
        if player.disco_active:
            return False
            
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        angle = math.degrees(math.atan2(-dy, dx)) % 360
        angle_diff = abs((self.direction * 180 - angle + 180) % 360 - 180)
        
        if distance < VISION_CONE_LENGTH and angle_diff < VISION_CONE_ANGLE/2:
            if not player.crouching:
                self.alerted = True
                self.alert_timer = 60
                self.image = self.alert_image
                return True
        return False

    def draw_vision_cone(self, screen, camera):
        angle_rad = math.radians(self.direction * 180)
        end_x = self.rect.centerx + VISION_CONE_LENGTH * math.cos(angle_rad)
        end_y = self.rect.centery - camera.offset.y
        
        points = [
            (self.rect.centerx - camera.offset.x, self.rect.centery - camera.offset.y),
            (end_x - camera.offset.x, end_y - camera.offset.y)
        ]
        
        angle_left = math.radians(self.direction * 180 - VISION_CONE_ANGLE/2)
        angle_right = math.radians(self.direction * 180 + VISION_CONE_ANGLE/2)
        
        left_x = self.rect.centerx + VISION_CONE_LENGTH * math.cos(angle_left) - camera.offset.x
        left_y = self.rect.centery - VISION_CONE_LENGTH * math.sin(angle_left) - camera.offset.y
        
        right_x = self.rect.centerx + VISION_CONE_LENGTH * math.cos(angle_right) - camera.offset.x
        right_y = self.rect.centery - VISION_CONE_LENGTH * math.sin(angle_right) - camera.offset.y
        
        cone_points = [
            (self.rect.centerx - camera.offset.x, self.rect.centery - camera.offset.y),
            (left_x, left_y),
            (right_x, right_y)
        ]
        
        vision_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(vision_surface, (*NEON_PINK, 50), cone_points)
        screen.blit(vision_surface, (0, 0))

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
        if self.alerted:
            alert_surf = pygame.Surface((self.rect.width, 20), pygame.SRCALPHA)
            pygame.draw.rect(alert_surf, (255, 0, 0, 150), (0, 0, self.rect.width, 20))
            screen.blit(alert_surf, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y - 25))
