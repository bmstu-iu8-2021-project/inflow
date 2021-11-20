#!/usr/bin/python3

from re import A
import threading
import os

from flask import Flask, render_template


import database
import routes


def init_server(app, config):
    db_pool = database.get_postgres_conn_pool(config["PG_VARS"])

    database.create_schema(db_pool, config["SCHEMA_FILEPATH"])

    tag_service = routes.TagService(db_pool)
    resource_service = routes.ResourceService(db_pool)

    services = {
        "tags": tag_service,
        "resources": resource_service,
    }

    resource_controller = routes.ResourceController(services)
    tag_controller = routes.TagController(services)

    def index():
        return render_template('inflow.html')
        # return 'Inflow!'
    def auth():
        return render_template('auth.html')

    app.add_url_rule('/', view_func=index, methods=["GET"])
    app.add_url_rule('/auth', view_func=auth, methods=["GET"])

    app.add_url_rule('/tags/all', '/tags/all', view_func=tag_controller.all, methods=['GET'])
    app.add_url_rule('/tags/create', '/tags/create', view_func=tag_controller.create, methods=['POST'])
    app.add_url_rule('/tags/delete', '/tags/delete', view_func=tag_controller.delete, methods=['DELETE'])
    app.add_url_rule('/tags/search', '/tags/search', view_func=tag_controller.search, methods=['GET'])
    app.add_url_rule('/tags/join', '/tags/join', view_func=tag_controller.join, methods=['PUT'])

    app.add_url_rule('/resources/status', '/resources/status', resource_controller.status, methods=["GET"])
    app.add_url_rule('/resources/search_by_tag', '/resources/search_by_tag', view_func=resource_controller.search_by_tags, methods=['GET'])
    app.add_url_rule('/resources/search_by_title', '/resources/search_by_title', view_func=resource_controller.search_by_title, methods=['GET'])
    app.add_url_rule('/resources/delete', '/resources/delete', view_func=resource_controller.delete, methods=['DELETE'])
    app.add_url_rule('/resources/create', '/resources/create', view_func=resource_controller.create, methods=['POST'])
    app.add_url_rule('/resources/update_add_tags', '/resources/update_add_tags', view_func=resource_controller.update_add_tags, methods=['PUT'])
    app.add_url_rule('/resources/update_delete_tags', '/resources/update_delete_tags', view_func=resource_controller.update_delete_tags, methods=['PUT'])




SERVER_CONFIG = {
    "SCHEMA_FILEPATH": os.environ.get("SCHEMA_FILEPATH"),
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

    debug = not bool(os.environ.get("DEBUG")) and os.environ.get("DEBUG", "").lower() != "true"

    if debug:
        print("DEBUG: on")

    init_server(app, SERVER_CONFIG)
    
    app.run(host=address, port=3000, load_dotenv=False, debug=debug)
