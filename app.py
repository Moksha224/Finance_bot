from flask import Flask, request
import requests
import os
from db import create_table, insert_expense, get_history, clear_expenses

app = Flask(__name__)
create_table()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
user_states = {}

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=data)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "OK"
    
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    user_id = data["message"]["from"]["id"]

    if text == "/start":
        send_message(chat_id, "Welcome! Send me a category like 'Food' to begin.")
    elif text == "/history":
        send_message(chat_id, get_history(user_id))
    elif text == "/clear":
        clear_expenses(user_id)
        send_message(chat_id, "History cleared.")
    else:
        try:
            amount = float(text)
            category = user_states.pop(user_id, "Misc")
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"Added ₹{amount} to {category}")
        except:
            user_states[user_id] = text
            send_message(chat_id, f"Enter amount for {text}:")
    
    return "OK"
