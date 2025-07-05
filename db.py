# File: db.py

import sqlite3

DB_NAME = "expenses.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            user_id INTEGER,
            category TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_expense(user_id, category, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT category, amount, timestamp FROM expenses WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "📭 No expenses found."

    response = "🧾 Your Expense History:\n"
    total = 0
    for category, amount, timestamp in rows:
        response += f"• {category}: ₹{amount} on {timestamp[:10]}\n"
        total += amount
    response += f"\n💰 Total Spent: ₹{total}"
    return response

def clear_expenses(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
