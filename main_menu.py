import pygame
import sys
import cv2
import numpy as np

# Initialize Pygame
pygame.init()
pygame.font.init()

# Load your uploaded background
background = pygame.image.load('./assets/backgrounds/mainbackground.png')
background = pygame.transform.scale(background, (800, 600))

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retro Runway - Main Menu")

# Load retro font
retro_font_path = './assets/fonts/PressStart2P-Regular.ttf'  # Make sure this exists
font = pygame.font.Font(retro_font_path, 20)  # Main button font
small_font = pygame.font.Font(retro_font_path, 12)  # Instructions font

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 200)
HOVER_COLOR = (70, 70, 250)

# Variables
show_instructions = False
image_captured = False
captured_image = None

# Button Class
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Functions
def open_instructions():
    global show_instructions
    show_instructions = True

def quit_game():
    pygame.quit()
    sys.exit()

def capture_image():
    global captured_image, image_captured
    cap = cv2.VideoCapture(0)

    capturing = True
    while capturing:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Capture Image - Press (c) to capture, (r) to recapture, (q) to quit without capturing', frame)
        key = cv2.waitKey(1)

        if key == ord('c'):
            captured_image = frame
            image_captured = True
            print("Image Captured. Press (d) to Done, (r) to Recapture, (q) to Quit Without Saving.")
        elif key == ord('d') and image_captured:
            cv2.imwrite('captured_image.png', captured_image)
            print("Image saved as captured_image.png")
            capturing = False
        elif key == ord('r'):
            print("Recapturing...")
            image_captured = False
        elif key == ord('q'):
            print("Exiting without saving.")
            image_captured = False
            capturing = False

    cap.release()
    cv2.destroyAllWindows()

# Buttons
buttons = [
    Button('INSTRUCTIONS', 250, 200, 300, 50, open_instructions),
    Button('START CAPTURE', 250, 300, 300, 50, capture_image),
    Button('QUIT GAME', 250, 400, 300, 50, quit_game)
]

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_click(event)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Modal for instructions
    if show_instructions:
        modal_rect = pygame.Rect(150, 100, 500, 400)
        pygame.draw.rect(screen, BLACK, modal_rect)
        pygame.draw.rect(screen, WHITE, modal_rect, 2)

        instructions = [
            "Instructions:",
            "- Sneak past bouncers.",
            "- Collect retro items (glasses, shoes, jacket).",
            "- Hide behind objects if needed.",
            "- Reach the VIP entrance fully dressed!",
            "",
            "Press 'CLOSE' to return."
        ]

        for idx, line in enumerate(instructions):
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (modal_rect.x + 20, modal_rect.y + 20 + idx * 40))

        close_button = Button('CLOSE', modal_rect.x + 220, modal_rect.y + 350, 150, 40, lambda: setattr(sys.modules[__name__], 'show_instructions', False))
        close_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                close_button.check_click(event)

    pygame.display.flip()

pygame.quit()
