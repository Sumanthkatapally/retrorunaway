import pygame
from game import Game
from ui import UI
from sound_manager import SoundManager
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Retro Runway")
    clock = pygame.time.Clock()
    
    sound_manager = SoundManager()
    ui = UI()
    game = None
    
    current_state = "menu"  # menu, game, controls
    sound_manager.play_music("menu_theme.mp3")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if current_state == "menu":
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
                    sound_manager.play_music("menu_theme.mp3")
            
            elif current_state == "controls":
                if event.type == pygame.KEYDOWN:
                    current_state = "menu"

        # Draw appropriate screen
        if current_state == "menu":
            ui.draw_menu(screen)
        
        elif current_state == "game":
            game.handle_events()
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
            
            for i, control in enumerate(controls):
                text = ui.font_small.render(control, True, DISCO_BLUE)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i * 40))
            
            back = ui.font_small.render("Press any key to return", True, RETRO_YELLOW)
            screen.blit(back, (SCREEN_WIDTH//2 - back.get_width()//2, 550))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
