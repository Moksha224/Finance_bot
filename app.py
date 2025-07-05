# app.py
import os
import sqlite3
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
user_states = {}  # Temporary category selection per user

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=data)

def create_buttons():
    categories = ["Food", "Travel", "Groceries", "Snacks", "Health"]
    buttons = [[{"text": cat}] for cat in categories]
    return {"keyboard": buttons, "one_time_keyboard": True, "resize_keyboard": True}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "OK"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    user_id = data["message"]["from"]["id"]

    if text == "/start":
        send_message(chat_id, "Welcome! Select a category to begin:", reply_markup=create_buttons())
    elif text == "/history":
        history = get_user_history(user_id)
        send_message(chat_id, history)
    elif user_id in user_states:
        category = user_states.pop(user_id)
        try:
            amount = float(text)
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"✅ Recorded {amount} under {category}.")
        except ValueError:
            send_message(chat_id, "❌ Invalid amount. Please enter a number.")
    elif text in ["Food", "Travel", "Groceries", "Snacks", "Health"]:
        user_states[user_id] = text
        send_message(chat_id, f"Enter amount for {text}:")
    elif text == "/clear":
        clear_user_expenses(user_id)
        send_message(chat_id, "🗑️ Your expenses have been cleared.")
    else:
        send_message(chat_id, "Please choose a category first:", reply_markup=create_buttons())

    return "OK"
