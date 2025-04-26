import pygame
from game import Game
from ui import UI
from sound_manager import SoundManager
from constants import *

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    except pygame.error:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Retro Runway")
    clock = pygame.time.Clock()
    
    sound_manager = SoundManager()
    ui = UI()
    game = None
    
    current_state = "menu"  # menu, game, controls
    sound_manager.play_music("menu_theme")
    
    # Try loading the background image
    try:
        # Construct the file path using os.path.join
        bg_path = os.path.join(ASSETS_DIR, "Images", "background.png")
        menu_background = pygame.image.load(bg_path).convert()  # convert for faster blitting
        menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit the screen
        # Get the rectangle of the background image
        bg_rect = menu_background.get_rect()  # Changed from self.bg_rect since this isn't in a class
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading background image: {e}")
        menu_background = None
        bg_rect = None  # Also set bg_rect to None since it won't be defined if image load fails


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == "menu":
                # Draw the background first
                screen.fill(BLACK)  # Fill with black in case background fails to load
                if menu_background:
                    screen.blit(menu_background, (0, 0))
                ui.draw_menu(screen)  # Draw menu UI after background
                result = ui.handle_input(event)
                if result == "Start Game":
                    current_state = "game"
                    game = Game()
                    sound_manager.stop_music()
                elif result == "Controls":
                    current_state = "controls"
                elif result == "Quit":
                    running = False
            
            elif current_state == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = "menu"
                    game = None
                    sound_manager.play_music("menu_theme")
            
            elif current_state == "controls":
                if event.type == pygame.KEYDOWN:
                    current_state = "menu"

        # Draw appropriate screen
        if current_state == "menu":
            # Menu background and UI are handled above
            pass
        
        elif current_state == "game":
            game.handle_events()
            game.update()
            game.draw()
        
        elif current_state == "controls":
            screen.fill(BLACK)
            title = ui.font_large.render("CONTROLS", True, NEON_PINK)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            controls = [
                "Arrow Keys: Move",
                "Down: Crouch/Hide",
                "Space: Jump",
                "Up: Collect Items",
                "Shift: Activate Disco Power",
                "ESC: Return to Menu"
            ]
            
            for i, control in enumerate(controls):
                text = ui.font_small.render(control, True, DISCO_BLUE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250 + i * 40))
            
            back = ui.font_small.render("Press any key to return", True, RETRO_YELLOW)
            screen.blit(back, (SCREEN_WIDTH // 2 - back.get_width() // 2, 550))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
