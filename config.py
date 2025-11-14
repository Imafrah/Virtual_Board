import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# AI Settings
AI_MODEL = os.getenv('AI_MODEL', 'gemini-1.5-flash')
AI_MAX_RESPONSE_LINES = 5

# Camera Settings
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_INDEX = 0

# Hand Detection Settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_NUM_HANDS = 1

# Drawing Settings
DEFAULT_BRUSH_SIZE = 5
DEFAULT_COLOR = (0, 255, 0)  # Yellow (BGR)
PINCH_THRESHOLD = 0.05

# Keyboard Settings
KEY_WIDTH = 80
KEY_HEIGHT = 80
KEY_MARGIN = 10
HOVER_THRESHOLD = 1  # seconds

# Sketch Settings
SKETCH_DIR = os.getenv('SKETCH_DIR', 'sketches')
THUMBNAIL_SIZE = (100, 75)