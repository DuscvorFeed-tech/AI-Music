# config.py
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Drive
SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json"
)
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

# Shader & rendering defaults
WIDTH = int(os.getenv("WIDTH", 512))
HEIGHT = int(os.getenv("HEIGHT", 512))
FPS = int(os.getenv("FPS", 30))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "temp/frames")
SHADER_PATH = os.getenv("SHADER_PATH", "temp/shader.frag")
VIDEO_PATH = os.getenv("VIDEO_PATH", os.path.join("temp", "generated_video.mp4"))
