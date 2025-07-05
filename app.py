# app.py
from db import create_table, insert_expense, get_history, clear_expenses
import os
import sqlite3
from flask import Flask, request
import requests

create_table()

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
user_states = {}  # Temporary category selection per user

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    print("Sending message:", data)
    response = requests.post(f"{BOT_URL}/sendMessage", json=data)
    print("Telegram response:", response.text)

def create_buttons():
    categories = ["Food", "Travel", "Groceries", "Snacks", "Health"]
    buttons = [[{"text": cat}] for cat in categories]
    return {"keyboard": buttons, "one_time_keyboard": True, "resize_keyboard": True}

def create_main_menu():
    buttons = [
        [{"text": "/history"}],
        [{"text": "/clear"}],
        [{"text": "Add Expense"}]
    ]
    return {"keyboard": buttons, "resize_keyboard": True}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "OK"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    user_id = data["message"]["from"]["id"]

    if text == "/start" or text == "Add Expense":
        send_message(chat_id, "Welcome! Select a category to begin:", reply_markup=create_buttons())

    elif text == "/history":
        history = get_history(user_id)
        send_message(chat_id, history, reply_markup=create_main_menu())

    elif text == "/clear":
        clear_expenses(user_id)
        send_message(chat_id, "🗑️ Your expenses have been cleared.", reply_markup=create_main_menu())

    elif user_id in user_states:
        category = user_states.pop(user_id)
        try:
            amount = float(text)
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"✅ Recorded {amount} under {category}.", reply_markup=create_main_menu())
        except ValueError:
            send_message(chat_id, "❌ Invalid amount. Please enter a number.")
            user_states[user_id] = category  # Ask again until valid

    elif text in ["Food", "Travel", "Groceries", "Snacks", "Health"]:
        user_states[user_id] = text
        send_message(chat_id, f"Enter amount for {text}:")

    else:
        send_message(chat_id, "Please choose an option:", reply_markup=create_main_menu())

    return "OK"
