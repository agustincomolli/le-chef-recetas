"""
Inicialización de la aplicación Flask.

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from app.config import Config
from .routes.main import main
from .routes.auth import auth

db = SQLAlchemy()


def create_app():
    """
    Crea una instancia de aplicación Flask con configuración básica.

    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Configuración
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app
