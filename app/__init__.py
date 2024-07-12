"""
Inicialización de la aplicación Flask.

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from app.config import Config

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
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
   
    return app
