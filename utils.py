# utils.py

import requests
from config import BOT_URL

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=payload)

def create_category_buttons():
    categories = ["Food", "Travel", "Groceries", "Snacks", "Health"]
    keyboard = [[{"text": category}] for category in categories]
    return {
        "keyboard": keyboard,
        "one_time_keyboard": True,
        "resize_keyboard": True
    }
