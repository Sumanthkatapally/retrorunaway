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

# Variables
show_instructions = False
image_captured = False
captured_image = None
show_camera = False
camera_buttons = []
close_button = None  # Initialize close_button variable
show_live_feed = True  # Add this with other global variables

# Gradient colors for main menu buttons
PURPLE = (142, 45, 226)  # #8e2de2
BLUE = (74, 0, 224)      # #4a00e0

# Button Class
class Button:
    def __init__(self, text, x, y, w, h, callback, font=button_font):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.font = font

    def draw(self, surface, gradient=False):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        if gradient:
            # Draw gradient background
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
    if not image_captured:
        camera_buttons = [
            Button('Capture', 200, 500, 120, 40, capture_current_frame),
            Button('Continue Without', 340, 500, 200, 40, continue_without_capture)
        ]
    else:
        camera_buttons = [
            Button('Click', 200, 500, 120, 40, take_snapshot),
            Button('Done', 340, 500, 120, 40, finish_capture)
        ]

def capture_current_frame():
    global image_captured
    image_captured = True
    create_camera_buttons()  # Update buttons to show Click and Done

def take_snapshot():
    global captured_image, image_captured, camera_buttons, show_live_feed
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            captured_image = frame
            show_live_feed = False  # Don't show live feed after capture
            # Update buttons to show Recapture and Done
            camera_buttons = [
                Button('Recapture', 200, 500, 120, 40, recapture_image),
                Button('Done', 340, 500, 120, 40, finish_capture)
            ]

def recapture_image():
    global image_captured, camera_buttons, show_live_feed
    show_live_feed = True  # Show live feed when recapturing
    # Update buttons back to Click and Done
    camera_buttons = [
        Button('Click', 200, 500, 120, 40, take_snapshot),
        Button('Done', 340, 500, 120, 40, finish_capture)
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
        pygame.draw.rect(screen, BLACK, modal_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, modal_rect, 2, border_radius=10)

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

            # Create circular mask
            mask = pygame.Surface((400, 300), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (200, 150), 150)
            
            # Apply mask to frame
            frame.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw circular background
            pygame.draw.circle(screen, CIRCLE_COLOR, (400, 300), 160)
            
            # If we have a captured image and not showing live feed, show the captured image
            if not show_live_feed and captured_image is not None:
                # Convert captured image to Pygame surface
                preview = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
                preview = np.rot90(preview)
                preview = pygame.surfarray.make_surface(preview)
                preview = pygame.transform.scale(preview, (400, 300))
                preview.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(preview, (200, 150))
            else:
                # Show live feed
                screen.blit(frame, (200, 150))

            # Draw camera buttons
            for button in camera_buttons:
                button.draw(screen)

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
