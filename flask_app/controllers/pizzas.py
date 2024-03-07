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


pizza_orders = []


@app.route("/order", methods=["POST"])
def create_pizza():
    method = request.form.get("method")
    crust = request.form.get("crust")
    size = request.form.get("size")
    quantity = request.form.get("quantity")
    toppings = request.form.getlist("toppings")

    # Validate the form data (you can add more validation as needed)
    if not method or not crust or not size or not quantity or not toppings:
        flash("Please fill out all fields.", "error")
        return redirect("/")

    # Save the order to the mockup database (replace with actual database interaction)
    pizza_order = {
        "method": method,
        "crust": crust,
        "size": size,
        "quantity": quantity,
        "toppings": toppings,
    }
    pizza_orders.append(pizza_order)

    flash("Pizza order created successfully!", "success")
    # Redirect to the validation page
    return redirect("pizza.html")


@app.route("/pizza", methods=["POST"])
def validation_page():
    # Retrieve the order details from the database (replace with actual database interaction)
    last_order = pizza_orders[-1] if pizza_orders else None
    return render_template("pizza.html", order=last_order)


"""@app.route("/order", methods=["POST"])
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
        "toppings": request.form["toppings"],
        "user_id": session["user_id"],  # id e personit te loguar
    }
    Pizza.create(data)
    return redirect("/")
"""


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
