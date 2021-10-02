#!/usr/bin/python3

import psycopg2
import sys
import threading

from flask import Flask
from flask.views import View

app = Flask(__name__)

import services



class Server:

    def __init__(self, host, port, config):
        self.host = host
        self.port = port
        # переменная app в которой лежит объект класса Flask, инициализируем объект через __name__
        self.app = Flask(__name__)
        # andpoint для выключения приложения
        # в view_func= передаем параметр, который будет выполнять функцию shutdown

        self.tag_service = services.TagService(SERVER_CONFIG["DB_VARS"])
        
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/tags/all', view_func=self.tags_all, methods=['GET'])

    def run(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def get_home(self):
        return 'Welcome to the inflow!'

    
    def tags_all(self):
        return str(self.tag_service.all())
            

SERVER_CONFIG = {
    "DB_VARS": {
        "PG_USER": "inflow-client",
        "PG_PASS": "QwerTY",
        "PG_DB": "inflow",
        "PG_PORT":"5432",
        "PG_HOST": "localhost",
    }
}

if __name__ == "__main__":

    
    server = Server("127.0.0.1", "3000", SERVER_CONFIG)
    server.run()