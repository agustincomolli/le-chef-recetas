"""
Este módulo contiene las funciones que tocarán la base de datos.
"""

from sqlalchemy import text
from app import db


def insert_categories() -> None:
    """
    Crea las categorías iniciales en la base de datos.

    Returns:
        None
    """
    categories = ["Bebidas", "Entradas", "Platos principales", "Postres", "Otros"]
    # Iniciar una transacción.
    with db.engine.begin() as connection:
        # Si hay categorías, salir de la función.
        if connection.execute(text("SELECT COUNT(*) FROM categories")).scalar():
            return

        for category in categories:
            connection.execute(text("INSERT INTO categories (name) VALUES (:name)"),
                               {"name": category})
        # Si alguna de las operaciones falla, se realiza un rollback automáticamente.


def get_categories() -> list[str]:
    """
    Obtiene una lista de nombres de categorías desde la base de datos.

    Esta función ejecuta una consulta SQL para seleccionar todos los nombres de 
    las categorías de la tabla 'categories', y retorna una lista con estos nombres.

    Returns:
        list: Una lista de nombres de categorías obtenidos de la base de datos.
    """
    result = db.session.execute(text("SELECT name FROM categories;"))
    categories = [category[0] for category in result.fetchall()]
    return categories
