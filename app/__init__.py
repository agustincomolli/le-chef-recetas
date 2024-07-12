"""
Inicialización de la aplicación Flask.

"""
from flask import Flask
from flask_session import Session
from config import Config


def create_app():
    """
    Crea una instancia de aplicación Flask con configuración básica.
    
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Registrar blueprints
    from app import routes
    app.register_blueprint(routes.bp)

    return app
