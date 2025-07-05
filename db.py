from datetime import datetime
from collections import defaultdict

# In-memory store
expenses = defaultdict(list)

def insert_expense(user_id, category, amount):
    expenses[user_id].append({
        "amount": amount,
        "category": category,
        "timestamp": datetime.now()
    })

def get_monthly_total(user_id):
    now = datetime.now()
    return sum(e["amount"] for e in expenses[user_id] if e["timestamp"].month == now.month)

def get_category_summary(user_id):
    summary = defaultdict(float)
    for e in expenses[user_id]:
        summary[e["category"]] += e["amount"]
    return summary.items()
