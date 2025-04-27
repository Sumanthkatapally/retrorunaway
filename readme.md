# 🎮 Retro Runaway - Stealth Adventure Game

[![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?logo=pygame)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🌉 Sneak past bouncers, collect retro items, and blend into the disco crowd in this vibrant stealth game built in Python with Pygame!

---

## 🚀 Features

- 🕶️ **Stealth Mechanics:** Hide behind objects and dodge patrolling bouncers.
- 🚵️ **Collectibles:** Gather retro clothing and items to upgrade your look.
- 🎵 **Dynamic Sounds:** Engaging retro-style sound effects and background music.
- 🌉 **Retro Pixel Art:** Neon-lit cityscape with vibrant visual style.
- 🎯 **Camera and Hiding Spots:** Utilize obstacles for strategic gameplay.
- 🎮 **Menu System:** Interactive game start, instructions, and webcam capture options.

---

## 📂 Project Structure

```
gamehackathon/
└── src/
    ├── assets/            # Images, sprites, audio assets
    ├── bouncer.py         # Bouncer (enemy) AI
    ├── collectible.py     # Collectible item logic
    ├── constants.py       # Global constants for the game
    ├── game.py            # Core game loop and logic
    ├── hiding_spot.py     # Hiding spot logic
    ├── level.py           # Level design and layout
    ├── main.py            # Main entry point
    ├── player.py          # Player character logic
    ├── sound_manager.py   # Manages sounds and music
    └── ui.py              # UI rendering and interaction
```

---

## 📦 Requirements

- Python 3.7 or higher
- `pygame`
- `opencv-python`

Install all dependencies:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install pygame opencv-python
```

---

## 🛠️ Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sumanthkatapally/retrorunaway.git
   cd retrorunaway/gamehackathon/src
   ```

2. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r ../../requirements.txt
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

---

## 🎮 Gameplay Controls

| Action                  | Key                |
|--------------------------|--------------------|
| Move Left                | A or Left Arrow     |
| Move Right               | D or Right Arrow    |
| Move Up                  | W or Up Arrow       |
| Move Down                | S or Down Arrow     |

---

## 📋 TODO & Future Improvements

- Add more levels and challenges 🌆
- Enhance bouncer AI behavior 🧠
- Power-ups and speed boosts 🏃
- Multiplayer local co-op mode 👩‍👩‍👧

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🎨 Acknowledgements

- Inspired by **80s Disco Era** and **Retro Pixel Art**
- Built with ❤️ using [Pygame](https://www.pygame.org/) and [OpenCV](https://opencv.org/)