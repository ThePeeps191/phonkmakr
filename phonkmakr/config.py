import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SESSIONS_DIR = PROJECT_ROOT / "sessions"
SESSIONS_DIR.mkdir(exist_ok = True)

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok = True)

SAMPLES_DIR = PROJECT_ROOT / "samples"
SAMPLES_DIR.mkdir(exist_ok = True)
SAMPLE_SOURCES_JSON = PROJECT_ROOT / "phonkmakr" / "samples" / "sources.json"

# Deepseek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-flash"

# Agent
MAX_TOOL_ROUNDS = 55
MAX_ITERATIONS = 3  # how many times agent can re-analyze and fix
MODEL_TEMPERATURE = 0.8

# Audio Defaults
DEFAULT_BPM = 130
DEFAULT_KEY = "Cm"
DEFAULT_BARS = 32
SAMPLE_RATE = 44100
BIT_DEPTH = 16
DEFAULT_FORMAT = "mp3"

# edge-tts voices
TTS_VOICES = {
    "male": "pt-BR-AntonioNeural",
    "female": "pt-BR-FranciscaNeural",
    "male_deep": "pt-BR-DonatoNeural",
    "female_warm": "pt-BR-BrendaNeural",
}
