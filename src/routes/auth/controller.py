import sys
from flask import json
from flask.json import jsonify
import psycopg2

from flask import request

sys.path.append('..')

from .service import AuthService
from models import User
from utils import Singleton

class AuthController(metaclass=Singleton):

    def __init__(self, services: dict):
        # TODO: raise exception if services doesn't contain "resources"
        self.users: AuthService = services.get("users")

    def create(self): 
        jsonbody: dict = request.get_json(force=True)

        # TODO: check keys
        if "login" and "password" in jsonbody:
            login: str = jsonbody.get("login")
            password: str = jsonbody.get("password")

            # TODO: handle service's exceptions
            user: User = self.users.create(login, password)
            return jsonify(user)
        else:
            return {"error": "incorrect data entered"}