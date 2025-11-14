# 🎨 AirBoard - AI-Powered Touchless Whiteboard

An interactive computer-vision-based system that lets you draw, write, and interact using only hand gestures. No mouse, keyboard, or touchscreen needed! Built with Python, OpenCV, and MediaPipe.

![AirBoard Demo](demo.gif)
*Screenshot: AirBoard in action with hand tracking and AI response panel*

## ✨ Features

- 🖐️ **Hand Tracking**: Real-time hand and finger detection using MediaPipe
- ✍️ **Air Drawing**: Draw in the air using pinch gestures
- ⌨️ **Virtual Keyboard**: Type using hover-based selection
- 🤖 **AI Assistant**: Integrated with Gemini via Google's API
- 💾 **Sketch Management**: Save and view your drawing history
- 🎨 **Dual Mode**: Toggle between drawing and keyboard modes
- 🚀 **Responsive UI**: Clean interface with visual feedback

## 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **OpenCV** - Computer vision and image processing
- **MediaPipe** - Hand tracking and gesture recognition
- **Google Gemini API** - AI-powered responses
- **NumPy** - Numerical operations
- **python-dotenv** - Environment variable management

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam
- Google Gemini API key (for AI features)
- pip (Python package manager)

## 🎥 Demo

[![Watch Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtube.com/shorts/YOUR_VIDEO_ID)

## 🚀 Installation

### 1. Clone or Download the Project
```bash
git clone <your-repo-url>
cd airboard
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv airboard_env
airboard_env\Scripts\activate

# Mac/Linux
python3 -m venv airboard_env
source airboard_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Key

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Get your Gemini API key
3. Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
python airboard.py
```

## 🎮 Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `M` | Toggle between Draw/Keyboard mode |
| `S` | Save current sketch |
| `C` | Clear canvas |
| `R` | Reset AI response |
| `H` | Toggle help display |
| `Q` | Quit application |

### Hand Gestures

**Draw Mode:**
- ✊ **Pinch** (thumb + index finger) - Start drawing
- ✋ **Release pinch** - Stop drawing
- 👆 **Single finger up** - Move cursor without drawing

**Keyboard Mode:**
- 👆 **Hover** over a key (1 second to select)
- ✋ **Hold position** - Select key
- ✅ **SEND button** - Submit your query to AI

## 📂 Project Structure

```
airboard/
├── airboard.py              # Main application
├── config.py                # Configuration settings
├── requirements.txt         # Dependencies
├── .env                     # API keys (create this)
├── .gitignore               # Git ignore rules
├── README.md                # This file
│
├── modules/
│   ├── __init__.py
│   ├── hand_tracker.py     # Hand detection and tracking
│   ├── keyboard.py         # Virtual keyboard implementation
│   ├── drawing.py          # Canvas and drawing logic
│   ├── ai_assistant.py     # Gemini AI integration
│   └── sketch_manager.py   # Save/load sketches
│
└── sketches/               # Directory for saved sketches (auto-created)
```

## ⚙️ Configuration (config.py)

Customize the application by modifying `config.py`:

```python
# Camera Settings
CAMERA_INDEX = 0          # Try 0, 1, 2 if camera not detected
CAMERA_WIDTH = 1280       # Camera frame width (higher for better resolution)
CAMERA_HEIGHT = 720       # Camera frame height (720p is recommended for performance)

# Hand Detection
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_NUM_HANDS = 1         # Number of hands to detect

# Drawing
DEFAULT_BRUSH_SIZE = 5
DEFAULT_COLOR = (0, 255, 0)  # Green (BGR format)
PINCH_THRESHOLD = 0.05       # Sensitivity for pinch detection

# Keyboard
KEY_WIDTH = 80        # Width of each key
KEY_HEIGHT = 80       # Height of each key
KEY_MARGIN = 10       # Space between keys
HOVER_THRESHOLD = 1   # Seconds to hover before key press

# File Paths
SKETCH_DIR = 'sketches'  # Directory to save sketches
THUMBNAIL_SIZE = (100, 75)  # Size of sketch thumbnails
MAX_NUM_HANDS = 2

# Drawing settings
DEFAULT_BRUSH_SIZE = 5    # Brush size in pixels
DEFAULT_COLOR = (0, 165, 255)  # Orange color (BGR format)

# Keyboard settings
KEY_WIDTH = 60            # Width of each key
KEY_HEIGHT = 60           # Height of each key
KEY_MARGIN = 5            # Space between keys
HOVER_THRESHOLD = 1.5     # Seconds to hover before key press

# AI settings
AI_MODEL = "meta-llama/llama-3.2-3b-instruct:free"
MAX_TOKENS = 500          # Maximum length of AI response
TEMPERATURE = 0.7         # Lower for more focused, higher for more creative

# UI settings
SHOW_FPS = True           # Show frames per second counter
SHOW_LANDMARKS = False    # Show hand landmarks (for debugging)
```

## 🚀 Getting Started

### Drawing Mode
1. Run the application: `python airboard.py`
2. Make a pinch gesture (thumb to index finger) to start drawing
3. Move your hand to draw on the virtual canvas
4. Release the pinch to stop drawing
5. Press `S` to save your sketch

### Keyboard Mode
1. Press `M` to switch to keyboard mode
2. Hover over keys to highlight them
3. Hold position for 1 second to select a key
4. Type your question and hover over SEND to get AI response
5. Press `R` to clear the AI response

### 🎨 Drawing Mode

1. **Start Drawing**
   - Make a pinch gesture (thumb to index finger) to start drawing
   - Move your hand to create lines on the canvas
   - Release the pinch to stop drawing

2. **Saving Your Work**
   - Press `S` to save the current sketch
   - Sketches are automatically saved with timestamps
   - View saved sketches in the gallery at the bottom

3. **Drawing Tools**
   - Press `C` to clear the canvas
   - Use two fingers up gesture to cycle through brush sizes
   - Press `R` to clear the AI response panel

### ⌨️ Keyboard Mode

1. **Switching Modes**
   - Press `M` to toggle between Draw and Keyboard modes
   - The mode indicator in the top-left shows current mode

2. **Typing**
   - Hover over keys to highlight them
   - Hold position for 1.5 seconds to select a key
   - For faster typing, make a quick tap gesture

3. **AI Interaction**
   - Type your question using the virtual keyboard
   - Hover over `SEND` to submit your query
   - AI responses appear in the side panel
   - Press `R` to clear the response panel

### 💡 Pro Tips
- Ensure good lighting for better hand tracking
- Keep your hand steady when selecting keys
- For best results, position your hand parallel to the camera
- The system works best with a solid background

## 🛠️ Troubleshooting

### Common Issues

**Camera Not Working**
- Check if another application is using the camera
- Verify camera permissions in your OS
- Try different `CAMERA_INDEX` values (0, 1, 2, etc.)

**Hand Not Detected**
- Ensure good lighting conditions
- Keep your hand within the camera frame
- Adjust `MIN_DETECTION_CONFIDENCE` in config.py

**AI Not Responding**
- Check your internet connection
- Verify your Gemini API key in `.env`
- Ensure you have sufficient API quota

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **Google Gemini** for AI capabilities
- **OpenCV** for computer vision
- **Python** community for amazing libraries

### Common Issues

#### Camera Not Working
```python
# Try these solutions:
# 1. Check if another application is using the camera
# 2. Try different CAMERA_INDEX values (0, 1, 2, etc.)
# 3. Verify camera permissions in your OS settings
```

#### Hand Detection Problems
- Ensure your hand is well-lit and visible
- Try moving closer to/farther from the camera
- Adjust `MIN_DETECTION_CONFIDENCE` in config.py
- Make sure your hand is not too close to the edges of the frame

#### Performance Issues
- Lower the camera resolution in config.py
- Close other resource-intensive applications
- Reduce `MAX_NUM_HANDS` to 1 if you only need single-hand tracking
- Set `SHOW_LANDMARKS = False` for better performance

#### AI Integration
- Verify your OpenRouter API key is correct
- Check your internet connection
- Ensure you have sufficient credits in your OpenRouter account
- Try a different AI model if responses are slow

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. Format code:
   ```bash
   black .
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe for the excellent hand tracking
- OpenRouter for AI model access
- OpenCV for computer vision capabilities

### Camera Not Detected
```python
# Try different camera indices in config.py
CAMERA_INDEX = 0  # Try 1, 2, etc.
```

### Hand Detection Issues

- Ensure good lighting
- Position your hand clearly in frame
- Adjust detection confidence in `config.py`:
```python
MIN_DETECTION_CONFIDENCE = 0.5  # Lower for easier detection
```

### API Errors

- Verify your API key in `.env`
- Check internet connection
- Ensure OpenRouter account has credits

### Performance Issues

- Lower camera resolution in `config.py`
- Close other applications
- Reduce `MAX_NUM_HANDS` to 1

## 🎨 Customization Ideas

### Change Drawing Color
```python
# In config.py
DEFAULT_COLOR = (255, 0, 0)  # Red (BGR format)
```

### Add New Gestures
```python
# In modules/hand_tracker.py
def is_thumbs_up(self, hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    thumb_mcp = hand_landmarks.landmark[2]
    return thumb_tip.y < thumb_mcp.y
```

### Custom Keyboard Layout
```python
# In modules/keyboard.py
self.keys = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    # ... your custom layout
]
```

## 🐛 Known Issues

- Hand tracking may lag on slower systems
- AI responses can take 3-10 seconds
- Pinch gesture requires practice for precision

## 🚀 Future Enhancements

- [ ] Multi-color drawing palette
- [ ] Gesture-based undo/redo
- [ ] Export sketches as PDF/SVG
- [ ] Collaborative multiplayer mode
- [ ] Voice command integration
- [ ] 3D depth tracking
- [ ] Mobile app version

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **OpenCV** for computer vision
- **OpenRouter** for AI model access
- **Meta** for LLaMA models

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Email: your-email@example.com
- Discord: your-discord

## 🌟 Show Your Support

If you found this project helpful, please give it a ⭐️!

---

**Made with ❤️ by [Your Name]** #   V i r t u a l _ B o a r d 
 
 
