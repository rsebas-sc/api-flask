from flask import Flask
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)
    from . import routes

    routes.init_app(app)

    return app