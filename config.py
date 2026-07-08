import os
from pathlib import Path
from dotenv import load_dotenv

# Попытка загрузить стандартный `.env`, иначе — `doc.env` (в репозитории)
if Path(".env").exists():
	load_dotenv(".env")
elif Path("doc.env").exists():
	load_dotenv("doc.env")
else:
	# fallback: load from default locations / environment
	load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
AI_TOKEN = os.getenv("AI_TOKEN")