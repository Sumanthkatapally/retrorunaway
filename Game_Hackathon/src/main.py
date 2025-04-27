# File: src/main.py

import os
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
    current_state = "menu"
    sound_manager.play_music("menu_theme")

    # Load menu background
    try:
        bg_path = os.path.join(ASSETS_DIR, "Images", "background.png")
        menu_background = pygame.image.load(bg_path).convert()
        menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_rect = menu_background.get_rect()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading background image: {e}")
        menu_background = None
        bg_rect = None

    running = True
    while running:
        # **Pull all events once** per frame
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # --- MENU STATE ---
            if current_state == "menu":
                # draw menu each event so click highlights smoothly
                screen.fill(BLACK)
                if menu_background:
                    screen.blit(menu_background, (0, 0))
                ui.draw_menu(screen)

                result = ui.handle_input(event)
                if result == "Start Game":
                    current_state = "game"
                    game = Game()
                    sound_manager.stop_music()
                elif result == "Controls":
                    current_state = "controls"
                elif result == "Quit":
                    running = False

            # --- GAME STATE ---
            elif current_state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # back to menu
                        current_state = "menu"
                        game = None
                        sound_manager.play_music("menu_theme")
                    elif event.key == pygame.K_SPACE:
                        # jump
                        game.player.jump()
                    elif event.key == pygame.K_UP:
                        # collect items
                        game.check_collectibles()

            # --- CONTROLS SCREEN ---
            elif current_state == "controls":
                if event.type == pygame.KEYDOWN:
                    current_state = "menu"

        # --- UPDATE & DRAW ---
        if current_state == "game":
            game.update()
            game.draw()

        elif current_state == "controls":
            screen.fill(BLACK)
            title = ui.font_large.render("CONTROLS", True, NEON_PINK)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

            controls = [
                "Arrow Keys: Move",
                "Down: Crouch/Hide",
                "Space: Jump",
                "Up: Collect Items",
                "Shift: Activate Disco Power",
                "ESC: Return to Menu"
            ]
            for i, c in enumerate(controls):
                text = ui.font_small.render(c, True, DISCO_BLUE)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*40))

            back = ui.font_small.render("Press any key to return", True, RETRO_YELLOW)
            screen.blit(back, (SCREEN_WIDTH//2 - back.get_width()//2, 550))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
