import pygame
import sys
import cv2
import numpy as np
import os  # Add this import
import atexit
import time

# Initialize Pygame
pygame.init()
pygame.font.init()

# Load your uploaded background
background = pygame.image.load('./assets/backgrounds/mainbackground.png')
background = pygame.transform.scale(background, (800, 600))

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retro Runway - Main Menu")


# Fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 200)
HOVER_COLOR = (70, 70, 250)
MODAL_COLOR = (0, 0, 0, 200)  # Semi-transparent black
CIRCLE_COLOR = (40, 40, 40)
PURPLE = (142, 45, 226)  # #8e2de2
BLUE = (74, 0, 224)      # #4a00e0
PURPLE_MODAL = (142, 45, 226, 240)  # Rich purple, slightly transparent
DARK_PURPLE_TOP = (75, 0, 110)
DARK_PURPLE_BOTTOM = (26, 0, 51)

# Variables
show_instructions = False
image_captured = False
captured_image = None
show_camera = False
camera_buttons = []
close_button = None  # Initialize close_button variable
show_live_feed = True  # Add this with other global variables

# Button Class
class Button:
    def __init__(self, text, x, y, w, h, callback, font=button_font):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.font = font

    def draw(self, surface, gradient=False, color_override=None):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        if color_override is not None:
            pygame.draw.rect(surface, color_override, self.rect, border_radius=10)
        elif gradient:
            draw_gradient_rect(surface, self.rect, PURPLE, BLUE)
        else:
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Functions
def open_instructions():
    global show_instructions, close_button
    show_instructions = True
    # Create close button when instructions are opened
    close_button = Button('Close', 350, 420, 100, 40, 
                         lambda: setattr(sys.modules[__name__], 'show_instructions', False))

def quit_game():
    # Try to delete the file before quitting
    try:
        abs_path = os.path.abspath('captured_image.png')
        if os.path.exists(abs_path):
            os.remove(abs_path)
            print('captured_image.png deleted in quit_game.')
        else:
            print('captured_image.png not found in quit_game.')
    except Exception as e:
        print(f"Error deleting captured_image.png in quit_game: {e}")
    pygame.quit()
    sys.exit()

def create_camera_buttons():
    global camera_buttons
    # Initial state: Click and Exit
    camera_buttons = [
        Button('Click', 200, 500, 120, 40, take_snapshot),
        Button('Exit', 340, 500, 120, 40, finish_capture)
    ]

def take_snapshot():
    global captured_image, image_captured, camera_buttons, show_live_feed
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            captured_image = frame
            image_captured = True  # Mark that an image has been captured
            show_live_feed = False  # Don't show live feed after capture
            # After Click: Recapture and Done
            camera_buttons = [
                Button('Recapture', 200, 500, 120, 40, recapture_image),
                Button('Done', 340, 500, 120, 40, finish_capture)
            ]

def recapture_image():
    global image_captured, camera_buttons, show_live_feed
    show_live_feed = True  # Show live feed when recapturing
    # Return to Click and Exit
    camera_buttons = [
        Button('Click', 200, 500, 120, 40, take_snapshot),
        Button('Exit', 340, 500, 120, 40, finish_capture)
    ]

def finish_capture():
    global show_camera, image_captured
    if image_captured and captured_image is not None:
        cv2.imwrite('captured_image.png', captured_image)
    show_camera = False
    cap.release()

def continue_without_capture():
    global show_camera, image_captured
    image_captured = False
    show_camera = False
    cap.release()

def capture_image():
    global show_camera, cap
    show_camera = True
    cap = cv2.VideoCapture(0)
    create_camera_buttons()

def draw_gradient_rect(surface, rect, color1, color2):
    """Draw a vertical gradient from color1 (top) to color2 (bottom) in the given rect."""
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))

def draw_gradient_circle(surface, center, radius, color1, color2, width=10):
    """Draw a circular gradient border from color1 to color2."""
    for i in range(width):
        ratio = i / width
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.circle(surface, (r, g, b), center, radius - i, 1)

# Buttons
# Place menu in the top right corner
button_width = 320
button_height = 50
button_margin_top = 40
button_margin_right = 40
button_gap = 30
button_x = 800 - button_width - button_margin_right
button_y_start = button_margin_top

buttons = [
    Button('View Instructions', button_x, button_y_start, button_width, button_height, open_instructions),
    Button('Start by Capturing Image', button_x, button_y_start + button_height + button_gap, button_width, button_height, capture_image),
    Button('Quit Game', button_x, button_y_start + 2 * (button_height + button_gap), button_width, button_height, quit_game)
]

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Try to delete the file before quitting
            try:
                abs_path = os.path.abspath('captured_image.png')
                if os.path.exists(abs_path):
                    os.remove(abs_path)
                    print('captured_image.png deleted on window close.')
                else:
                    print('captured_image.png not found on window close.')
            except Exception as e:
                print(f"Error deleting captured_image.png on window close: {e}")
            running = False
        for button in buttons:
            button.check_click(event)
        if show_camera:
            for button in camera_buttons:
                button.check_click(event)
        if show_instructions and close_button:
            close_button.check_click(event)

    # Draw buttons
    for button in buttons:
        button.draw(screen, gradient=True)  # Use gradient for main menu

    # Modal for instructions
    if show_instructions:
        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill(MODAL_COLOR)
        screen.blit(overlay, (0, 0))

        modal_rect = pygame.Rect(150, 100, 500, 400)
        # Draw dark purple gradient modal background
        modal_surface = pygame.Surface((500, 400), pygame.SRCALPHA)
        for i in range(400):
            ratio = i / 400
            r = int(DARK_PURPLE_TOP[0] * (1 - ratio) + DARK_PURPLE_BOTTOM[0] * ratio)
            g = int(DARK_PURPLE_TOP[1] * (1 - ratio) + DARK_PURPLE_BOTTOM[1] * ratio)
            b = int(DARK_PURPLE_TOP[2] * (1 - ratio) + DARK_PURPLE_BOTTOM[2] * ratio)
            pygame.draw.line(modal_surface, (r, g, b, 230), (0, i), (500, i))
        pygame.draw.rect(modal_surface, WHITE, modal_surface.get_rect(), 2, border_radius=10)
        screen.blit(modal_surface, (150, 100))

        instructions = [
            "Instructions:",
            "- Sneak past bouncers.",
            "- Collect retro items (glasses, shoes, jacket).",
            "- Hide behind objects if needed.",
            "- Reach the VIP entrance fully dressed!",
            "",
            "Click the 'Close' button below to return."
        ]

        for idx, line in enumerate(instructions):
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (modal_rect.x + 20, modal_rect.y + 20 + idx * 40))

        # Position the close button at the bottom of the modal
        if close_button:
            close_button.rect.x = modal_rect.centerx - 50  # Center the button horizontally
            close_button.rect.y = modal_rect.bottom - 60   # Position near the bottom
            close_button.draw(screen)

    # Camera view
    if show_camera and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV frame to Pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (400, 300))

            # Create a transparent surface for the circular camera feed
            cam_surface = pygame.Surface((400, 300), pygame.SRCALPHA)
            cam_surface.fill((0, 0, 0, 0))  # Fully transparent

            # Create a circular mask
            mask = pygame.Surface((400, 300), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 0))
            pygame.draw.circle(mask, (255, 255, 255, 255), (200, 150), 150)

            # Decide what to show: captured image or live feed
            if not show_live_feed and captured_image is not None:
                # Show the captured image
                preview = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
                preview = np.rot90(preview)
                preview = pygame.surfarray.make_surface(preview)
                preview = pygame.transform.scale(preview, (400, 300))
                preview.set_colorkey((0, 0, 0))
                cam_surface.blit(preview, (0, 0))
                cam_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                # Show the live feed
                frame.set_colorkey((0, 0, 0))
                cam_surface.blit(frame, (0, 0))
                cam_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Draw gradient border (no black rectangle)
            circle_center = (400, 300)
            draw_gradient_circle(screen, circle_center, 160, PURPLE, BLUE, width=16)

            # Blit the circular camera feed (transparent outside the circle)
            screen.blit(cam_surface, (200, 150))

            # Center the camera buttons below the circle
            total_button_width = sum([button.rect.width for button in camera_buttons]) + 40 * (len(camera_buttons) - 1)
            start_x = 400 - total_button_width // 2
            button_y = 480
            x = start_x
            for button in camera_buttons:
                button.rect.x = x
                button.rect.y = button_y
                button.draw(screen, color_override=BLACK)
                x += button.rect.width + 40

    pygame.display.flip()

pygame.quit()

def cleanup_captured_image():
    try:
        # Wait a moment to ensure file is released
        time.sleep(0.2)
        abs_path = os.path.abspath('captured_image.png')
        if os.path.exists(abs_path):
            os.remove(abs_path)
            print('captured_image.png deleted by atexit.')
        else:
            print('captured_image.png not found by atexit.')
    except Exception as e:
        print(f"Error deleting captured_image.png in atexit: {e}")

atexit.register(cleanup_captured_image)
