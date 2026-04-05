from flask import Flask, render_template, request, redirect, session
from users import users
import os
from stock_db import db, StockItem, Sale, Expense
from stock_manager import (
    get_stock_page_data,
    add_item,
    mark_as_sold,
    update_status,
    delete_item,
    add_expense,
    delete_expense,
    revert_sold
)

from motor import bot_inicio, bot_prompt, bot_processar

app = Flask(__name__)
app.secret_key = "supersecretkey"

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL não está definida.")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username

            # iniciar conversa do bot na sessão
            session["bot_state"] = bot_inicio()
            session["history"] = [
                {"role": "bot", "text": bot_prompt(session["bot_state"])}
            ]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Credenciais inválidas")

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    reset_msg = session.pop("reset_message", None)

    # garante estruturas
    if "bot_state" not in session:
        session["bot_state"] = bot_inicio()
    if "history" not in session:
        session["history"] = [{"role": "bot", "text": bot_prompt(session["bot_state"])}]

    resultado = None  # ✅ define antes de usar

    if request.method == "POST":
        user_msg = request.form["input_text"].strip()

        # (opcional) ignorar submits vazios
        if user_msg:
            # guardar user msg
            session["history"].append({"role": "user", "text": user_msg})

            # obter resposta do bot (a tua lógica)
            bot_reply, novo_estado = bot_processar(session["bot_state"], user_msg)
            session["bot_state"]=novo_estado
            # guardar bot msg
            session["history"].append({"role": "bot", "text": bot_reply})

            # se a tua função alterar o estado, volta a guardar
            session.modified = True

    return render_template(
        "dashboard.html",
        history=session["history"],
        reset_msg=reset_msg
    )

@app.route("/reset")
def reset():
    if "user" not in session:
        return redirect("/")
    session.pop("bot_state", None)
    session.pop("history", None)
    session["reset_message"] = "✅ Nova avaliação iniciada. Conversa anterior apagada."
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("bot_state", None)
    session.pop("history", None)
    return redirect("/")

@app.route("/stock")
def stock():
    if "user" not in session:
        return redirect("/")

    username = session["user"]

    stock_items = StockItem.query.filter(
        StockItem.username == username,
        StockItem.quantity > 0
    ).order_by(StockItem.id.desc()).all()

    sold_items = Sale.query.filter_by(username=username).order_by(Sale.id.desc()).all()
    expenses = Expense.query.filter_by(username=username).order_by(Expense.id.desc()).all()

    total_stock_quantity = sum(item.quantity for item in stock_items)
    total_sold_quantity = sum(item.quantity_sold for item in sold_items)

    total_inventory_spend = (
        sum(item.quantity * item.buy_price for item in stock_items)
        + sum(sale.quantity_sold * sale.buy_price for sale in sold_items)
    )

    total_extra_expenses = sum(exp.cost for exp in expenses)
    total_spent = total_inventory_spend + total_extra_expenses
    total_revenue = sum(sale.quantity_sold * sale.sold_price for sale in sold_items)
    gross_profit = total_revenue - total_spent

    return render_template(
        "stock.html",
        stock_items=stock_items,
        sold_items=sold_items,
        expenses=expenses,
        total_stock_quantity=total_stock_quantity,
        total_sold_quantity=total_sold_quantity,
        total_inventory_spend=round(total_inventory_spend, 2),
        total_extra_expenses=round(total_extra_expenses, 2),
        total_spent=round(total_spent, 2),
        total_revenue=round(total_revenue, 2),
        gross_profit=round(gross_profit, 2)
    )


@app.route("/stock/add-item", methods=["POST"])
def stock_add_item():
    if "user" not in session:
        return redirect("/")

    username = session["user"]

    item = StockItem(
        username=username,
        name=request.form["name"].strip(),
        brand=request.form.get("brand", "").strip(),
        category=request.form.get("category", "").strip(),
        quantity=int(request.form["quantity"]),
        buy_date=request.form["buy_date"],
        buy_price=float(request.form["buy_price"]),
        status=request.form["status"],
        platform=request.form.get("platform", "").strip(),
        location=request.form.get("location", "").strip(),
        notes=request.form.get("notes", "").strip()
    )

    db.session.add(item)
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/update-status/<int:item_id>", methods=["POST"])
def stock_update_status(item_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    item = StockItem.query.filter_by(id=item_id, username=username).first_or_404()

    item.status = request.form["status"]
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/mark-sold/<int:item_id>", methods=["POST"])
def stock_mark_sold(item_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    item = StockItem.query.filter_by(id=item_id, username=username).first_or_404()

    sold_quantity = int(request.form["sold_quantity"])
    sold_price = float(request.form["sold_price"])
    sold_date = request.form["sold_date"]

    if sold_quantity < 1 or sold_quantity > item.quantity:
        return redirect("/stock")

    sale = Sale(
        username=username,
        stock_item_id=item.id,
        name=item.name,
        brand=item.brand,
        category=item.category,
        quantity_sold=sold_quantity,
        buy_date=item.buy_date,
        buy_price=item.buy_price,
        sold_date=sold_date,
        sold_price=sold_price,
        platform=item.platform,
        location=item.location,
        notes=item.notes
    )

    item.quantity -= sold_quantity

    if item.quantity == 0:
        db.session.delete(item)

    db.session.add(sale)
    db.session.commit()

    return redirect("/stock")


@app.route("/stock/revert-sale/<int:sale_id>", methods=["POST"])
def stock_revert_sale(sale_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    sale = Sale.query.filter_by(id=sale_id, username=username).first_or_404()

    existing_item = StockItem.query.filter_by(
        username=username,
        name=sale.name,
        brand=sale.brand,
        category=sale.category,
        buy_date=sale.buy_date,
        buy_price=sale.buy_price,
        platform=sale.platform,
        location=sale.location,
        notes=sale.notes
    ).first()

    if existing_item:
        existing_item.quantity += sale.quantity_sold
        existing_item.status = "Comprado"
    else:
        new_item = StockItem(
            username=username,
            name=sale.name,
            brand=sale.brand,
            category=sale.category,
            quantity=sale.quantity_sold,
            buy_date=sale.buy_date,
            buy_price=sale.buy_price,
            status="Comprado",
            platform=sale.platform,
            location=sale.location,
            notes=sale.notes
        )
        db.session.add(new_item)

    db.session.delete(sale)
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/delete-item/<int:item_id>", methods=["POST"])
def stock_delete_item(item_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    item = StockItem.query.filter_by(id=item_id, username=username).first_or_404()

    db.session.delete(item)
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/delete-sale/<int:sale_id>", methods=["POST"])
def stock_delete_sale(sale_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    sale = Sale.query.filter_by(id=sale_id, username=username).first_or_404()

    db.session.delete(sale)
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/add-expense", methods=["POST"])
def stock_add_expense():
    if "user" not in session:
        return redirect("/")

    username = session["user"]

    expense = Expense(
        username=username,
        name=request.form["name"].strip(),
        category=request.form.get("category", "").strip(),
        quantity=int(request.form["quantity"]),
        date=request.form["date"],
        cost=float(request.form["cost"]),
        notes=request.form.get("notes", "").strip()
    )

    db.session.add(expense)
    db.session.commit()
    return redirect("/stock")


@app.route("/stock/delete-expense/<int:expense_id>", methods=["POST"])
def stock_delete_expense(expense_id):
    if "user" not in session:
        return redirect("/")

    username = session["user"]
    expense = Expense.query.filter_by(id=expense_id, username=username).first_or_404()

    db.session.delete(expense)
    db.session.commit()
    return redirect("/stock")

if __name__ == "__main__":
    app.run()
