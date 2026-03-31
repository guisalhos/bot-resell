from flask import Flask, render_template, request, redirect, session
from users import users

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

    return render_template("stock.html")

if __name__ == "__main__":
    app.run()
