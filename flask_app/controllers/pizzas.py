from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.pizza import Pizza


@app.route("/pizzas")
def pizzas():
    if "user_id" in session:
        return render_template("pizzas.html")
    return redirect("/")


@app.route("/order")
def order():
    if "user_id" in session:
        return render_template("order.html")
    return redirect("/")


@app.route("/pizzas/new")
def addPizza():
    if "user_id" in session:
        return render_template("addPizza.html")

    return redirect("/")


@app.route("/pizza", methods=["POST"])
def createPizza():
    if "user_id" not in session:
        return redirect("/")
    if not Pizza.validate_pizza(request.form):
        return redirect(request.referrer)
    data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "quantity": request.form["quantity"],
        "user_id": session["user_id"],  # id e personit te loguar
    }
    Pizza.create(data)
    return redirect("/")


@app.route("/pizza/<int:id>")
def viewpizza(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id, "pizza_id": id}
    pizza = pizza.get_pizza_by_id(data)
    return redirect("/")


@app.route("/pizza/delete/<int:id>")
def deletepizza(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    pizza = Pizza.get_pizza_by_id(data)
    if pizza["user_id"] == session["user_id"]:
        Pizza.delete(data)
    return redirect("/")
