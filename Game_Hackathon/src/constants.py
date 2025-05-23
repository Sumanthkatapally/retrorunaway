# File: src/constants.py
import os

ASSETS_DIR    = os.path.join(os.path.dirname(__file__), 'assets')
EFFECTS_PATH  = os.path.join(ASSETS_DIR, 'sounds', 'Effects')
MUSIC_PATH    = os.path.join(ASSETS_DIR, 'sounds', 'Music')
IMAGES_PATH   = os.path.join(ASSETS_DIR, 'Images')

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
GRAVITY       = 0.75
JUMP_STRENGTH = -15
PLAYER_SPEED  = 5
BOUNCER_SPEED = 2
VISION_CONE_ANGLE  = 60
VISION_CONE_LENGTH = 300
DISCO_DURATION     = 5000
TILE_SIZE     = 64

NEON_PINK     = (255,20,147)
DISCO_BLUE    = (30,144,255)
RETRO_YELLOW  = (255,255,0)
BLACK         = (0,0,0)

OUTFIT_ORDER = ['Bell-Bottom','Disco-Shirt','Sunglasses','Shoe','hair']

LEVELS = [
    {
      'name': 'Disco Parking Lot',
      'bg_color': (20,20,40),
      'music': 'level1_theme.mp3',
      'enemies': 3,
      'collectibles': ['Bell-Bottom','Disco-Shirt'],
      # parking lot uses cars by name
    },
    {
      'name': 'Neon Nightclub',
      'bg_color': (10,10,30),
      'music': 'level2_theme.mp3',
      'enemies': 5,
      'collectibles': ['Sunglasses','Shoe','hair'],
      # explicitly request cars here as well
      'hiding_spots': 'cars'
    }
]
