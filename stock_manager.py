import json
import os
from datetime import datetime

DATA_DIR = "data"
STOCK_FILE = os.path.join(DATA_DIR, "stock_data.json")

DEFAULT_DATA = {
    "items": [],
    "expenses": []
}


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(STOCK_FILE):
        with open(STOCK_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=2, ensure_ascii=False)


def load_data():
    ensure_data_file()
    with open(STOCK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_item_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def generate_expense_id(expenses):
    if not expenses:
        return 1
    return max(exp["id"] for exp in expenses) + 1


def add_item(form):
    data = load_data()
    items = data["items"]

    quantity = int(form["quantity"])
    buy_price = float(form["buy_price"])

    item = {
        "id": generate_item_id(items),
        "name": form["name"].strip(),
        "brand": form.get("brand", "").strip(),
        "category": form.get("category", "").strip(),
        "quantity": quantity,
        "buy_date": form["buy_date"],
        "buy_price": buy_price,
        "status": form["status"],
        "platform": form.get("platform", "").strip(),
        "location": form.get("location", "").strip(),
        "notes": form.get("notes", "").strip(),
        "sold_price": None,
        "sold_date": None
    }

    items.append(item)
    save_data(data)


def mark_as_sold(item_id, sold_price, sold_date):
    data = load_data()

    for item in data["items"]:
        if item["id"] == item_id:
            item["status"] = "Vendido"
            item["sold_price"] = float(sold_price)
            item["sold_date"] = sold_date
            break

    save_data(data)


def update_status(item_id, new_status):
    data = load_data()

    for item in data["items"]:
        if item["id"] == item_id:
            item["status"] = new_status
            break

    save_data(data)


def delete_item(item_id):
    data = load_data()
    data["items"] = [item for item in data["items"] if item["id"] != item_id]
    save_data(data)


def add_expense(form):
    data = load_data()
    expenses = data["expenses"]

    expense = {
        "id": generate_expense_id(expenses),
        "name": form["name"].strip(),
        "category": form.get("category", "").strip(),
        "quantity": int(form["quantity"]),
        "date": form["date"],
        "cost": float(form["cost"]),
        "notes": form.get("notes", "").strip()
    }

    expenses.append(expense)
    save_data(data)


def delete_expense(expense_id):
    data = load_data()
    data["expenses"] = [exp for exp in data["expenses"] if exp["id"] != expense_id]
    save_data(data)


def get_stock_page_data():
    data = load_data()
    items = data["items"]
    expenses = data["expenses"]

    stock_items = [item for item in items if item["status"] != "Vendido"]
    sold_items = [item for item in items if item["status"] == "Vendido"]

    total_stock_quantity = sum(item["quantity"] for item in stock_items)
    total_sold_quantity = sum(item["quantity"] for item in sold_items)

    total_inventory_spend = sum(item["quantity"] * item["buy_price"] for item in items)
    total_extra_expenses = sum(exp["cost"] for exp in expenses)
    total_spent = total_inventory_spend + total_extra_expenses

    total_revenue = sum(
        (item["sold_price"] or 0) * item["quantity"]
        for item in sold_items
    )

    gross_profit = total_revenue - total_spent

    return {
        "stock_items": stock_items,
        "sold_items": sold_items,
        "expenses": expenses,
        "total_stock_quantity": total_stock_quantity,
        "total_sold_quantity": total_sold_quantity,
        "total_inventory_spend": round(total_inventory_spend, 2),
        "total_extra_expenses": round(total_extra_expenses, 2),
        "total_spent": round(total_spent, 2),
        "total_revenue": round(total_revenue, 2),
        "gross_profit": round(gross_profit, 2)
    }