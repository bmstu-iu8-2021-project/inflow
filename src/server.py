#!/usr/bin/python3

from re import A
import threading
import os

from flask import Flask


import database
import routes


def init_server(app, config):
    db_connection = database.get_postgres_conntection(config["PG_VARS"])

    tag_service = routes.TagService(db_connection)
    resource_service = routes.ResourceService(db_connection)



    def index():
        return 'Inflow!'

    app.add_url_rule('/', view_func=index, methods=["GET"])

    app.add_url_rule('/tags/all', view_func=tag_service.all, methods=['GET'])
    app.add_url_rule('/tags/create', view_func=tag_service.create, methods=['POST'])
    app.add_url_rule('/tags/delete', view_func=tag_service.delete, methods=['DELETE'])
    app.add_url_rule('/tags/search', view_func=tag_service.search, methods=['GET'])
    app.add_url_rule('/tags/join', view_func=tag_service.join, methods=['PUT'])

    app.add_url_rule('/article/search_by_tag', view_func=resource_service.search_by_tag, methods=['GET'])
    app.add_url_rule('/article/search_by_label', view_func=resource_service.search_by_label, methods=['GET'])
    app.add_url_rule('/article/delete', view_func=resource_service.art_delete, methods=['DELETE'])
    app.add_url_rule('/article/create', view_func=resource_service.art_create, methods=['POST'])
    app.add_url_rule('/article/update_add_tags', view_func=resource_service.update_add_tags, methods=['PUT'])
    app.add_url_rule('/article/update_delete_tags', view_func=resource_service.update_delete_tags, methods=['PUT'])




SERVER_CONFIG = {
    "PG_VARS": {
        "PG_USER": os.environ.get("PG_USER"),
        "PG_PASS": os.environ.get("PG_PASS"),
        "PG_DB":   os.environ.get("PG_DB"),
        "PG_PORT": os.environ.get("PG_PORT"),
        "PG_HOST": os.environ.get("PG_HOST"),
    }
}

if __name__ == "__main__":
    app = Flask(__name__)
    
    address = os.environ.get("PROD_ADDR")
    if not address:
        address = "127.0.0.1"
    address = "0.0.0.0"

    init_server(app, SERVER_CONFIG)
    
    app.run(host=address, port=3000, load_dotenv=False)
