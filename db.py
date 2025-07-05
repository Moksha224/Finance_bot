import sqlite3

def create_table():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            user_id INTEGER,
            category TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_expense(user_id, category, amount):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT category, amount FROM expenses WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No expenses recorded."
    return "\n".join([f"{cat}: ₹{amt}" for cat, amt in rows])

def clear_expenses(user_id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
