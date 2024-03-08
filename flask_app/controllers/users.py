import math
import random

from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.user import User

bcrypt = Bcrypt(app)

import paypalrestsdk

ADMINEMAIL = "ardit.raseni@gmail.com"
PASSWORD = "ardit12345"


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/pizzas")
    return redirect("/logout")


@app.route("/register")
def registerPage():
    if "user_id" in session:
        return redirect("/pizzas")
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    if "user_id" in session:
        return redirect("/")
    if not User.validate_userRegister(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash("This account already exists", "emailRegister")
        return redirect(request.referrer)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "confirm_password": bcrypt.generate_password_hash(
            request.form["confirm_password"]
        ),
    }
    session["user_id"] = User.create(data)
    return redirect("/")


@app.route("/login")
def loginPage():
    if "user_id" in session:
        return redirect("/pizzas")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if not user:
        flash("This email doesnt exist", "emailLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user["password"], request.form["password"]):
        flash("Incorrect password", "passwordLogin")
        return redirect(request.referrer)

    session["user_id"] = user["user_id"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    return render_template("profile.html", loggedUser=User.get_user_by_id(data))


@app.route("/edit/user")
def editUser():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    return render_template("editUser.html", loggedUser=User.get_user_by_id(data))


@app.route("/edit/user", methods=["POST"])
def edit():
    if "user_id" not in session:
        return redirect("/")
    if not User.validate_userUpdate(request.form):
        return redirect(request.referrer)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "id": session["user_id"],
    }
    User.update(data)
    flash("User succesfully updated", "updateSuccess")
    return redirect(request.referrer)


@app.route("/delete/user")
def delete():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    User.delete(data)
    return redirect("/logout")


@app.route("/checkout/paypal")
def checkoutPaypal():
    if "user_id" not in session:
        return redirect("/")
    takeout = 200
    thick = 50
    big = 100
    quantity = 1
    toppings = 100
    totalPrice = round(takeout + thick + big + quantity + toppings)

    try:
        paypalrestsdk.configure(
            {
                "mode": "sandbox",  # Change this to "live" when you're ready to go live
                "client_id": "AYckYn5asNG7rR9A2gycCw-N2Du3GXH4ytNfU5ueLeYKaUwjKFL-aZMu3owCwfs_D1fydp2W-HSVieZ0",
                "client_secret": "EJu8H94UNn6b2Xigp26rf1pIs6NW-WrweGw-RkboWLUjWfHK2m46qrFObh_rL_HPSwvfipNyFoYdoa3K",
            }
        )

        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {
                            "total": totalPrice,
                            "currency": "USD",  # Adjust based on your currency
                        },
                        "description": f"Total to pay for the pizza",
                    }
                ],
                "redirect_urls": {
                    "return_url": url_for(
                        "paymentSuccess", _external=True, totalPrice=totalPrice
                    ),
                    "cancel_url": "http://example.com/cancel",
                },
            }
        )

        if payment.create():
            approval_url = next(
                link.href for link in payment.links if link.rel == "approval_url"
            )
            return redirect(approval_url)
        else:
            flash("Something went wrong with your payment", "creditCardDetails")
            return redirect(request.referrer)
    except paypalrestsdk.ResourceNotFound as e:
        flash("Something went wrong with your payment", "creditCardDetails")
        return redirect(request.referrer)


@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get("paymentId", "")
    payer_id = request.args.get("PayerID", "")
    try:
        paypalrestsdk.configure(
            {
                "mode": "sandbox",  # Change this to "live" when you're ready to go live
                "client_id": "AYckYn5asNG7rR9A2gycCw-N2Du3GXH4ytNfU5ueLeYKaUwjKFL-aZMu3owCwfs_D1fydp2W-HSVieZ0",
                "client_secret": "EJu8H94UNn6b2Xigp26rf1pIs6NW-WrweGw-RkboWLUjWfHK2m46qrFObh_rL_HPSwvfipNyFoYdoa3K",
            }
        )
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):

            ammount = request.args.get("totalPrice")
            status = "Paid"
            user_id = session["user_id"]
            data = {"ammount": ammount, "status": status, "user_id": user_id}
            User.createPayment(data)

            flash("Your payment was successful!", "paymentSuccessful")
            return redirect("/pizzas")
        else:
            flash("Something went wrong with your payment", "paymentNotSuccessful")
            return redirect("/")
    except paypalrestsdk.ResourceNotFound as e:
        flash("Something went wrong with your payment", "paymentNotSuccessful")
        return redirect("/pizzas")


@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash("Payment was canceled", "paymentCanceled")
    return redirect("/pizzas")
