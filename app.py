# app.py

from flask import Flask, request
import requests
import os
from db import create_table, insert_expense, get_history, clear_expenses

app = Flask(__name__)
create_table()

# Get bot token from environment (Render dashboard → Environment)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Used to temporarily store user category before asking amount
user_states = {}

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=data)

def create_buttons():
    categories = ["Food", "Travel", "Groceries", "Snacks", "Health"]
    keyboard = [[{"text": cat}] for cat in categories]
    return {
        "keyboard": keyboard,
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" not in data:
        return "OK"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user_id = message["from"]["id"]

    # Handle commands
    if text == "/start":
        send_message(chat_id, "👋 Welcome! Choose a category to add your expense:", reply_markup=create_buttons())
        return "OK"

    if text == "/history":
        history = get_history(user_id)
        send_message(chat_id, history)
        return "OK"

    if text == "/clear":
        clear_expenses(user_id)
        send_message(chat_id, "🧹 All your previous expenses have been cleared.")
        return "OK"

    # Check if user already chose a category, now expecting amount
    if user_id in user_states:
        category = user_states.pop(user_id)
        try:
            amount = float(text)
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"✅ Recorded ₹{amount} under '{category}'.")
        except ValueError:
            send_message(chat_id, "❌ Please enter a valid number.")
        return "OK"

    # If user selected a valid category, store and ask for amount
    categories = ["Food", "Travel", "Groceries", "Snacks", "Health"]
    if text in categories:
        user_states[user_id] = text
        send_message(chat_id, f"💰 Please enter the amount you spent on {text.lower()}:")
        return "OK"

    # Otherwise, show category suggestions again
    send_message(chat_id, "Please choose a category to start:", reply_markup=create_buttons())
    return "OK"

