
from flask import Flask, render_template, request, redirect, session, url_for
from models import init_db, get_user_by_email, create_user, check_password, create_order, get_orders_by_user
import os

app = Flask(__name__)
app.secret_key = "skyempirex_secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)
        if user and check_password(user["password"], password):
            session["user"] = user["email"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        nickname = request.form["nickname"]
        create_user(email, password, nickname)
        return redirect("/login")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    orders = get_orders_by_user(session["user"])
    return render_template("dashboard.html", orders=orders)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
