from flask import Flask, request
import requests
from config import TELEGRAM_TOKEN
from db import init_db, insert_expense, get_monthly_total, get_category_summary
from utils import extract_expense

app = Flask(__name__)
init_db()

BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

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
        send_message(chat_id, "👋 Welcome to Expense Bot!\nTell me your expenses like:\n'I spent ₹500 on food'\nOr ask:\n'How much I spent this month?'")
        return "ok"

    if "spent" in text.lower() or "add" in text.lower():
        amount, category = extract_expense(text)
        if amount and category:
            insert_expense(user_id, category, amount)
            send_message(chat_id, f"✅ Added ₹{amount} for {category}")
        else:
            send_message(chat_id, "❌ Sorry, I couldn't understand the amount or category.")
        return "ok"

    elif "how much" in text.lower() and "month" in text.lower():
        total = get_monthly_total(user_id)
        send_message(chat_id, f"💸 You've spent ₹{total:.2f} this month.")
        return "ok"

    elif "breakdown" in text.lower() or "category" in text.lower():
        breakdown = get_category_summary(user_id)
        if breakdown:
            msg = "📊 Spending Breakdown:\n"
            for cat, amt in breakdown:
                msg += f"• {cat.capitalize()}: ₹{amt:.2f}\n"
        else:
            msg = "No expenses yet!"
        send_message(chat_id, msg)
        return "ok"

    else:
        send_message(chat_id, "❓ Sorry, I didn't understand. Try:\n- I spent ₹200 on food\n- How much I spent this month?")
        return "ok"

    return "ok"
