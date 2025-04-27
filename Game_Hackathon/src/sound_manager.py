import os
import pygame
from constants import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.current_music = None
        # Mapping track names to file paths
        self.music_files = {
            "menu_theme": os.path.join(MUSIC_PATH, "menu_theme.mp3"),
            "level1_theme": os.path.join(MUSIC_PATH, "level1_theme.mp3"),
            "level2_theme": os.path.join(MUSIC_PATH, "level2_theme.mp3"),
            "victory_theme": os.path.join(MUSIC_PATH, "victory_theme.mp3"),
        }
        self.load_sounds()

    def load_sounds(self):
        # Load sound effects from EFFECTS_PATH
        os.makedirs(EFFECTS_PATH, exist_ok=True)
        try:
            for sound_file in os.listdir(EFFECTS_PATH):
                if sound_file.endswith(('.wav', '.mp3', '.ogg')):
                    name = os.path.splitext(sound_file)[0]
                    full_path = os.path.join(EFFECTS_PATH, sound_file)
                    if os.path.exists(full_path):
                        self.sounds[name] = pygame.mixer.Sound(full_path)
        except Exception as e:
            print(f"Sound loading error: {e}")

    def play_sound(self, name):
        # Play a sound effect if loaded
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, track_name):
        # Safely load and play background music, catching corrupt file errors
        if track_name in self.music_files:
            try:
                path = self.music_files[track_name]
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = track_name
            except pygame.error as e:
                # Handle corrupt or unreadable music files gracefully
                print(f"Warning: Could not load music '{track_name}': {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def fadeout_music(self, duration=1000):
        pygame.mixer.music.fadeout(duration)
