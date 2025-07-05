import re

def extract_expense(text):
    match = re.search(r'₹?(\d+)', text)
    category_match = re.search(r'on (\w+)', text.lower())
    if match and category_match:
        amount = float(match.group(1))
        category = category_match.group(1)
        return amount, category
    return None, None
