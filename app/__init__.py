"""
Inicialización de la aplicación Flask.

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from .config import Config
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

    with app.app_context():
        # # Las líneas comentadas con `# pylint: disable` son para evitar mensajes
        # # de advertencia del analizador de código pylint, ya que la importación
        # # se realiza dentro de la función para una mejor organización del código.

        # # pylint: disable=import-outside-toplevel
        # # pylint: disable=unused-import
        # from .models import Ingredient, Recipe, Step, User
        # db.create_all()
        init_db()

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # pylint: disable=import-outside-toplevel
    from .utils.database import get_categories
    @app.context_processor
    def inject_categorias():
        """
        Agrega la lista de categorías al contexto de la plantilla.

        Esta función es un procesador de contexto de Flask que inserta la lista de 
        categorías en el contexto global de las plantillas, permitiendo que esté 
        disponible para su uso en cualquier plantilla renderizada.

        Returns:
            dict: Un diccionario con la clave 'categories' que contiene la lista de categorías.
        """
        return {'categories': get_categories()}

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app


def init_db():
    """
    Inicializa la base de datos creando todas las tablas necesarias.

    Esta función debe ser llamada idealmente al inicio de la aplicación para asegurarse
    de que la estructura de la base de datos esté lista para su uso.

    Returns:
        None

    """
    # Las líneas comentadas con `# pylint: disable` son para evitar mensajes
    # de advertencia del analizador de código pylint, ya que la importación
    # se realiza dentro de la función para una mejor organización del código.

    # pylint: disable=import-outside-toplevel
    # pylint: disable=unused-import
    from .models import Category, Ingredient, Recipe, Step, User
    from .utils.database import insert_categories
    db.create_all()
    insert_categories()
