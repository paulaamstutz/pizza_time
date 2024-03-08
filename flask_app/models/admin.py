import re

from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+"
)

PASWORD_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Admin:
    db_name = "mvcuserpizza"

    def __init__(self, data):
        self.id = data["id"]
        self.firstName = data["firstName"]
        self.lastName = data["lastName"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_admin_by_email(cls, data):
        query = "SELECT * FROM admins where email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def create(cls, data):
        query = "INSERT INTO admins (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_admin_by_id(cls, data):
        query = "SELECT * FROM admins where id = %(admin_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailLoginAdmin")
            is_valid = False

        if len(user["password"]) < 1:
            flash("Password is required!", "passwordLoginAdmin")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_userRegister(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!", "emailRegisterAdmin")
            is_valid = False
        if len(user["password"]) < 1:
            flash("Password is required!", "passwordRegisterAdmin")
            is_valid = False
        if len(user["first_name"]) < 1:
            flash("First name is required!", "nameRegisterAdmin")
            is_valid = False
        if len(user["last_name"]) < 1:
            flash("Last name is required!", "last_nameRegisterAdmin")
            is_valid = False
        return is_valid
