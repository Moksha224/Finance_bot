# utils.py

import re

def extract_expense(text):
    # Matches inputs like: 200 food, ₹300 travel, add 400 shopping
    amount_match = re.search(r'(?:₹|rs)?\s*(\d+)', text.lower())
    category_match = re.search(r'(?:on\s+)?([a-zA-Z]+)$', text.lower())

    if amount_match and category_match:
        amount = float(amount_match.group(1))
        category = category_match.group(1)
        return amount, category
    return None, None

