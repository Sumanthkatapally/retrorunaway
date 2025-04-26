import pygame
from constants import *

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.selected = 0
        self.options = ["Start Game", "Controls", "Quit"]

    def draw_menu(self, screen):
        screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("RETRO RUNWAY", True, NEON_PINK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Options
        for i, option in enumerate(self.options):
            color = RETRO_YELLOW if i == self.selected else DISCO_BLUE
            text = self.font_small.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300 + i * 50))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None
