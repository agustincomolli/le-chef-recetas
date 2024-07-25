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
    categories = ["Ultimas", "Bebidas", "Entradas",
                  "Platos principales", "Postres", "Otros"]
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


def is_unique_username(username: str) -> bool:
    """
    Verifica si un nombre de usuario es único en la base de datos.

    Esta función consulta la tabla 'users' para determinar si el nombre de usuario 
    proporcionado ya existe. Si existe, retorna False; de lo contrario, retorna True.

    Args:
        username (str): El nombre de usuario a verificar.

    Returns:
        bool: True si el nombre de usuario es único, False si ya existe.
    """
    # Iniciar una transacción.
    with db.engine.begin() as connection:
        # Ejecutar la consulta para verificar si el nombre de usuario existe.
        result = connection.execute(text("SELECT id FROM users WHERE username = :username"),
                                    {'username': username}).fetchone()
        if result:
            return False
    return True


def is_unique_email(email: str) -> bool:
    """
    Verifica si un correo electrónico es único en la base de datos.

    Esta función consulta la tabla 'users' para determinar si el email 
    proporcionado ya existe. Si existe, retorna False; de lo contrario, retorna True.

    Args:
        email (str): El email a verificar.

    Returns:
        bool: True si el email es único, False si ya existe.
    """
    # Iniciar una transacción.
    with db.engine.begin() as connection:
        # Ejecutar la consulta para verificar si el nombre de usuario existe.
        result = connection.execute(text("SELECT id FROM users WHERE email = :email"),
                                    {'email': email}).fetchone()
        if result:
            return False
    return True


def add_user(username, email, password, profile_image) -> int:
    # Iniciar una transacción.
    with db.engine.begin() as connection:
        connection.execute(text(""))

    return 1
