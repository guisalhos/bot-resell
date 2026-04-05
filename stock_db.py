from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class StockItem(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)

    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=True)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    buy_date = db.Column(db.String(50), nullable=False)
    buy_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(100), nullable=False, default="Comprado")
    platform = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)

    stock_item_id = db.Column(db.Integer, nullable=True)

    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=True)

    quantity_sold = db.Column(db.Integer, nullable=False)
    buy_date = db.Column(db.String(50), nullable=False)
    buy_price = db.Column(db.Float, nullable=False)

    sold_date = db.Column(db.String(50), nullable=False)
    sold_price = db.Column(db.Float, nullable=False)

    platform = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)

    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)