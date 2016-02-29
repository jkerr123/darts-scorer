from hashlib import sha256
from database import Database

__author__ = 'jamie'

COLLECTION = "users"


class User(object):

    @staticmethod
    def register_user(email, password):
        if Database.insert(COLLECTION, {"email": email, "password": password}):
            return True

        return False

    @staticmethod
    def find_user(email):
        if Database.find_one(COLLECTION, {"email": email}):
            return True

    @staticmethod
    def check_login(email, password):
        # This method checks a login/password combo is correct
        user = User.find_user(email)
        if user is not None:
            password_encode = password.encode('utf-8')
            if user.encrypted_password == sha256(password_encode).hexdigest():
                return True
        return False
