# Retro Runway - Main Menu

A simple Python-based main menu screen for the Retro Runway game.

## Features

- **View Instructions**: Opens a modal window displaying game controls and objectives.
- **Start by Capturing Image**: Launches the webcam to capture a player image with options to capture, recapture, or continue without saving.
- **Quit Game**: Exits the application cleanly.
- **Background**: Uses a retro neon cityscape as the menu background.
- **State Tracking**: Maintains a boolean flag to indicate whether an image has been captured.

## Prerequisites

- Python 3.7 or higher
- `pygame` for the game UI
- `opencv-python` (cv2) for camera capture

## Installation

1. **Clone the repository** (or copy project files) into your local machine:
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **(Optional but recommended) Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t have a `requirements.txt`, install manually:
   ```bash
   pip install pygame opencv-python
   ```

## File Structure

```
RetroRunwayMainMenu/
├── main_menu.py        # Main Python script for menu screen
├── bf87e121-7ad3-4c4c-b715-56ba187beb33.png   # Background image
├── captured_image.png  # (Generated) Last captured image
├── requirements.txt    # Project dependencies
└── README.md           # Project overview and setup instructions
```

## Usage

1. **Run the main script**:
   ```bash
   python main_menu.py
   ```
2. **Interact with the menu**:
   - Click **View Instructions** to read game controls.
   - Click **Start by Capturing Image** to open your webcam:
     - Press `c` to capture an image.
     - Press `d` to save and finish.
     - Press `r` to discard and recapture.
     - Press `q` to exit without saving.
   - Click **Quit Game** to close the application.

3. **Captured images** will be saved as `captured_image.png` in the project folder.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`**: Ensure you installed `pygame` in the same environment you’re running the script in (see Installation steps).
- **No webcam detected**: Confirm your camera is connected and not in use by other apps.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue in the repository.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- Inspired by 80s/90s synthwave and pixel-art aesthetics.
- Built with [pygame](https://www.pygame.org/) and [OpenCV](https://opencv.org/).

