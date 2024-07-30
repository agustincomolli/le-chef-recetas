"""
Inicialización de la aplicación Flask.

"""
from flask import Flask, render_template
from flask_session import Session
from .config import Config
from .extensions import db
from .routes.main import main
from .routes.auth import auth
from .utils.helpers import apology


def create_app():
    """
    Crea una instancia de aplicación Flask con configuración básica.

    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    Session(app)

    # Configuración de sesión
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        init_db()

    # Las líneas comentadas con `# pylint: disable` son para evitar mensajes
    # de advertencia del analizador de código pylint, ya que la importación
    # se realiza dentro de la función para una mejor organización del código.
    # pylint: disable=import-outside-toplevel

    # Importaciones locales para evitar importaciones circulares
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

    @app.errorhandler(404)
    def page_not_found(error):  # pylint: disable=unused-argument
        """
        Manejador de errores para el código de estado HTTP 404 (No encontrado).

        Args:
            error (HTTPException): El objeto de excepción que contiene detalles sobre el error.

        Returns:
            Response: Una respuesta personalizada que incluye un mensaje de error y el 
                      código de estado 404.
        """
        # return apology("página no encontrada", 404)
        return render_template("error-404.html")

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
