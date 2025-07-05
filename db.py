import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            category TEXT,
            amount REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_expense(user_id, category, amount):
    date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, ?)",
              (user_id, category, amount, date))
    conn.commit()
    conn.close()

def get_monthly_total(user_id):
    now = datetime.now()
    start = now.strftime("%Y-%m-01")
    end = now.strftime("%Y-%m-%d")
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?", (user_id, start, end))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0

def get_category_summary(user_id):
    now = datetime.now()
    start = now.strftime("%Y-%m-01")
    end = now.strftime("%Y-%m-%d")
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("""
        SELECT category, SUM(amount) FROM expenses 
        WHERE user_id = ? AND date BETWEEN ? AND ?
        GROUP BY category
    """, (user_id, start, end))
    rows = c.fetchall()
    conn.close()
    return rows
