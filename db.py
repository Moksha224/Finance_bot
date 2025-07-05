import sqlite3

# ✅ Run once to create the table
def create_table():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        user_id TEXT,
        category TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# ✅ Insert new expense
def insert_expense(user_id, category, amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)",
              (user_id, category, amount))
    conn.commit()
    conn.close()

# ✅ Get all expenses
def get_history(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT category, amount, timestamp FROM expenses WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# ✅ Delete all expenses
def clear_expenses(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
