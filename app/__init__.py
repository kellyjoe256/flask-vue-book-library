# pylint: disable=unused-variable
import json
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import config
from app.models import db
from app.routes import create_routes

api = Api()
jwt = JWTManager()

create_routes(api)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return json.dumps(user.json())

    return app
