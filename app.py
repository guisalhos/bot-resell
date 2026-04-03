from flask import Flask, render_template, request, redirect, session
from users import users
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

    stock_data = get_stock_page_data(session["user"])
    return render_template("stock.html", **stock_data)


@app.route("/stock/add-item", methods=["POST"])
def stock_add_item():
    if "user" not in session:
        return redirect("/")

    add_item(session["user"], request.form)
    return redirect("/stock")


@app.route("/stock/mark-sold/<int:item_id>", methods=["POST"])
def stock_mark_sold(item_id):
    if "user" not in session:
        return redirect("/")

    sold_price = request.form["sold_price"]
    sold_date = request.form["sold_date"]
    mark_as_sold(session["user"], item_id, sold_price, sold_date)
    return redirect("/stock")


@app.route("/stock/update-status/<int:item_id>", methods=["POST"])
def stock_update_status(item_id):
    if "user" not in session:
        return redirect("/")

    new_status = request.form["status"]
    update_status(session["user"], item_id, new_status)
    return redirect("/stock")


@app.route("/stock/delete-item/<int:item_id>", methods=["POST"])
def stock_delete_item(item_id):
    if "user" not in session:
        return redirect("/")

    delete_item(session["user"], item_id)
    return redirect("/stock")


@app.route("/stock/add-expense", methods=["POST"])
def stock_add_expense():
    if "user" not in session:
        return redirect("/")

    add_expense(session["user"], request.form)
    return redirect("/stock")


@app.route("/stock/delete-expense/<int:expense_id>", methods=["POST"])
def stock_delete_expense(expense_id):
    if "user" not in session:
        return redirect("/")

    delete_expense(session["user"], expense_id)
    return redirect("/stock")

@app.route("/stock/revert-sold/<int:item_id>", methods=["POST"])
def stock_revert_sold(item_id):
    if "user" not in session:
        return redirect("/")

    revert_sold(session["user"], item_id)
    return redirect("/stock")

if __name__ == "__main__":
    app.run()
