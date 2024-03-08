from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.pizza import Pizza
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/register/admin")
def registerPageAdmin():
    if "admin_id" in session:
        return redirect("/adminPage")
    return render_template("registerAdmin.html")


@app.route("/registerAdmin", methods=["POST"])
def registerAdmin():
    if "admin_id" in session:
        return redirect("/")
    if not Admin.validate_userRegister(request.form):
        return redirect(request.referrer)
    user = Admin.get_admin_by_email(request.form)
    if user:
        flash("This account already exists", "emailRegister")
        return redirect(request.referrer)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    session["admin_id"] = Admin.create(data)
    return redirect("/admin")


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

    session["user_id"] = user["admin_id"]
    return redirect("/admin")


@app.route("/loginPage/admin")
def loginPageAdmin():
    if "user_id" in session:
        return render_template("adminPage.html")
    return render_template("adminLogin.html")


@app.route("/admin")
def adminPage():
    if "user_id" not in session:
        return redirect("/")

    data = {"id": session["admin_id"]}
    user = Admin.get_admin_by_id(data)

    if user and user["role"] == "admin":
        return render_template(
            "adminPage.html", loggedUser=user, pizzas=Pizza.get_all()
        )

    return redirect("/logout")
