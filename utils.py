import re

def extract_expense(text):
    match = re.search(r'₹?(\d+)', text)
    amount = float(match.group(1)) if match else None

    # Try to find category
    categories = ['food', 'travel', 'rent', 'groceries', 'shopping', 'bills']
    text = text.lower()
    category = None
    for cat in categories:
        if cat in text:
            category = cat
            break

    return amount, category
