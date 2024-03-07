from flask import flash, redirect, render_template, request, session
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.pizza import Pizza
from flask_app.models.user import Users

bcrypt = Bcrypt(app)


@app.route("/login/admin", methods=["POST"])
def loginAdmin():
    if "user_id" in session:
        return redirect("/")
    if not Admin.validate_user(request.form):
        return redirect(request.referrer)
    user = Admin.get_admin_by_email(request.form)
    if not user:
        flash("This email doesnt exist", "emailLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user["password"], request.form["password"]):
        flash("Incorrect password", "passwordLogin")

        return redirect(request.referrer)

    session["user_id"] = user["id"]
    print(f"Session Data: {session}")
    return redirect("/admin")


@app.route("/loginPage/admin")
def loginPageAdmin():
    if "user_id" in session:
        return redirect("/")
    return render_template("adminLogin.html")


@app.route("/admin")
def adminPage():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    user = Admin.get_admin_by_id(data)
    if user and user["role"] == "admin":
        return render_template(
            "adminPage.html", loggedUser=user, pizzas=Pizza.get_all()
        )
    return redirect("/logout")


"""
@app.route("/pizza/new")
def newPizza():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    user = Admin.get_admin_by_id(data)
    if user and user["role"] == "admin":
        return render_template("registerpizza.html")
    return redirect("/logout")"""
