from flask import Flask, request
import requests
import os
from utils import extract_expense
from db import insert_expense, get_monthly_total, get_category_summary
from config import TELEGRAM_TOKEN, BOT_URL

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"{BOT_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message["chat"]["id"]
    user_id = str(message["from"]["id"])

    if text.lower().startswith("/start"):
        send_message(chat_id, "👋 Welcome to Expense Bot! Type: 'I spent ₹500 on food'")
        return "ok"

    if "spent" in text.lower():
        amount, category = extract_expense(text)
        if amount and category:
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"✅ Added ₹{amount} for {category}")
        else:
            send_message(chat_id, "❌ Couldn't understand. Try: 'I spent ₹500 on food'")
        return "ok"

    if "how much" in text.lower() and "month" in text.lower():
        total = get_monthly_total(user_id)
        send_message(chat_id, f"💸 You've spent ₹{total:.2f} this month.")
        return "ok"

    if "breakdown" in text.lower():
        breakdown = get_category_summary(user_id)
        if breakdown:
            msg = "📊 Breakdown:\n"
            for cat, amt in breakdown:
                msg += f"• {cat.capitalize()}: ₹{amt:.2f}\n"
        else:
            msg = "No expenses found."
        send_message(chat_id, msg)
        return "ok"

    send_message(chat_id, "Try saying: 'I spent ₹300 on travel'")
    return "ok"
