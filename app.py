# app.py

from flask import Flask, request
import requests
from db import user_expenses
from utils import extract_expense
import os

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

# Send message
def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{URL}/sendMessage", json=data)

# Reply keyboard (suggestions)
def get_keyboard():
    return {
        "keyboard": [
            ["₹100 Food", "₹200 Travel"],
            ["₹300 Shopping", "₹150 Bills"],
            ["How much I spent?", "Show breakdown"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_id = str(chat_id)
    text = data["message"].get("text", "")

    # Commands
    if text.lower().startswith("/start"):
        send_message(
            chat_id,
            "👋 Welcome to Expense Bot!\n\n"
            "💡 Just send:\n"
            "• ₹100 food\n"
            "• 200 travel\n"
            "• how much I spent?\n\n"
            "Choose below ⬇️",
            reply_markup=get_keyboard()
        )
        return "ok"

    if "how much" in text.lower():
        total = sum(exp["amount"] for exp in user_expenses.get(user_id, []))
        send_message(chat_id, f"💰 You’ve spent ₹{total:.2f} so far.")
        return "ok"

    if "breakdown" in text.lower():
        breakdown = {}
        for exp in user_expenses.get(user_id, []):
            breakdown[exp["category"]] = breakdown.get(exp["category"], 0) + exp["amount"]

        if breakdown:
            reply = "\n".join([f"• {k.capitalize()}: ₹{v:.2f}" for k, v in breakdown.items()])
            send_message(chat_id, f"📊 Expense Breakdown:\n{reply}")
        else:
            send_message(chat_id, "No expenses added yet.")
        return "ok"

    # Add new expense
    amount, category = extract_expense(text)
    if amount and category:
        user_expenses.setdefault(user_id, []).append({"amount": amount, "category": category.lower()})
        send_message(chat_id, f"✅ Added ₹{amount} under <b>{category}</b>", reply_markup=get_keyboard())
    else:
        send_message(chat_id, "❓ I didn't understand. Try something like: ₹250 travel", reply_markup=get_keyboard())

    return "ok"
