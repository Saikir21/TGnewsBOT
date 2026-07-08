import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent

for env_path in (BASE_DIR / ".env", BASE_DIR / "doc.env"):
    if env_path.exists() and load_dotenv is not None:
        load_dotenv(env_path)
        break


def _read_env(name: str) -> str:
    return os.getenv(name, "").strip()


BOT_TOKEN = _read_env("BOT_TOKEN")
WEATHER_TOKEN = _read_env("WEATHER_TOKEN")
AI_TOKEN = _read_env("AI_TOKEN")