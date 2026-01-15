# Configuration file for Leafy Assistant

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = Path(__file__).parent / '.env'
load_dotenv(env_file)

# Audio Settings
SPEECH_RATE = int(os.getenv('SPEECH_RATE', 160))
SPEECH_VOLUME = float(os.getenv('SPEECH_VOLUME', 1.0))
LANGUAGE = os.getenv('LANGUAGE', 'en-in')

# Paths
MUSIC_DIR = os.path.expanduser("~/Music")  # Use user's music directory
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "kindpng_1259258.png")
NOTES_FILE = "leafy.txt"

# API Keys (loaded from .env)
WOLFRAM_API_KEY = os.getenv('WOLFRAM_API_KEY', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=in&apiKey="

# Application Paths (Platform-specific)
APP_PATHS = {
    "vscode": {
        "win32": "code",
        "darwin": "/Applications/Visual Studio Code.app/Contents/MacOS/Code",
        "linux": "code"
    },
    "chrome": {
        "win32": "chrome",
        "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "linux": "google-chrome"
    },
}

# Window Settings
WINDOW_TITLE = "Leafy"
BUTTON_TEXT = "Click me!"
EXIT_BUTTON_TEXT = "BYE"

# Debug mode
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
