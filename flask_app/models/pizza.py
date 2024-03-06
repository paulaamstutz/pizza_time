from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


class Pizza:
    db_name = "mvcuserpizza"

    def __init__(self, data):
        self.id = data["pizza_id"]
        self.title = data["method"]
        self.description = data["size"]
        self.nrOfPages = data["crust"]
        self.price = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO pizzas (method, size, crust, quantity, user_id) VALUES (%(method)s, %(size)s, %(crust)s, %(quantity)s, %(author)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pizzas;"
        results = connectToMySQL(cls.db_name).query_db(query)
        pizzas = []
        if results:
            for pizza in results:
                pizzas.append(pizza)
        return pizzas

    @classmethod
    def get_pizza_by_id(cls, data):
        query = "SELECT * FROM pizzas LEFT JOIN users on pizzas.user_id = users.id WHERE pizzas.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pizzas where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
