# config.py

import os

# Ensure you set this environment variable in Render dashboard or locally via .env file
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN not set in environment!")

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
