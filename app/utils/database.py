"""
Este módulo contiene las funciones que tocarán la base de datos.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db


def insert_categories() -> None:
    """
    Crea las categorías iniciales en la base de datos.

    Returns:
        None
    """
    categories = ["Bebidas", "Entradas", "Platos principales",
                  "Postres", "Otros"]
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
    result = db.session.execute(text("SELECT * FROM categories;"))
    categories = [{"id": category[0], "name": category[1]} for category in result.fetchall()]
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


def add_user(username: str, email: str, password: str, profile_image: bytes) -> int:
    """
    Agrega un nuevo usuario a la base de datos.

    Esta función inserta un nuevo registro en la tabla 'users' con el nombre de usuario,
    correo electrónico, contraseña y la imagen de perfil proporcionados. Si la operación
    es exitosa, retorna 0. En caso de error, retorna 1.

    Args:
        username (str): El nombre de usuario.
        email (str): El correo electrónico del usuario.
        password (str): La contraseña del usuario.
        profile_image (bytes): La imagen de perfil del usuario en formato binario.

    Returns:
        int: 0 si la operación es exitosa, 1 en caso de error.
    """

    # pylint: disable=broad-exception-caught

    try:
        # Iniciar una transacción.
        with db.engine.begin() as connection:
            sql = "INSERT INTO users (username, email, password, profile_image) "
            sql += "VALUES (:username, :email, :password, :profile_image);"
            values = {'username': username,
                      'email': email,
                      'password': password,
                      'profile_image': profile_image
                      }
            connection.execute(text(sql), values)
            return 0
    except Exception as e:
        print(f"Error al agregar usuario: {e}")
        return 1


def delete_user(user_id: int) -> int:
    """
    Elimina un usuario de la base de datos según su ID.

    Args:
        user_id (int): El ID del usuario a eliminar.

    Returns:
        int: 0 si el usuario se eliminó correctamente, 1 si ocurrió un error.
    """

    # pylint: disable=broad-exception-caught

    try:
        # Iniciar una transacción.
        with db.session.begin():
            sql = "DELETE FROM users WHERE id = :user_id;"
            db.session.execute(text(sql), {"user_id": user_id})
            return 0
    except SQLAlchemyError as e:
        # Manejar errores específicos de SQLAlchemy
        print(f"Error de base de datos al eliminar usuario: {e}")
        return 1
    except Exception as e:
        # Manejar cualquier otro error no esperado
        print(f"Error inesperado al eliminar usuario: {e}")
        return 1


def get_user(username: str) -> dict:
    """
    Obtiene la información de un usuario desde la base de datos.

    Esta función consulta la tabla 'users' para obtener todos los detalles del usuario 
    cuyo nombre de usuario coincide con el proporcionado. Retorna un diccionario con la 
    información del usuario si se encuentra, o None si no se encuentra.

    Args:
        username (str): El nombre de usuario del que se desea obtener la información.

    Returns:
        dict: Un diccionario con la información del usuario, o None si no se encuentra el usuario.
    """

    # pylint: disable=broad-exception-caught

    try:
        # Iniciar una transacción.
        with db.session.begin():
            sql = "SELECT * FROM users WHERE username = :username;"
            result = db.session.execute(
                text(sql), {"username": username}).fetchone()
            # Convertir el resultado en un diccionario, si no es None.
            if result:
                # Crear un diccionario con los valores por índice.
                user = {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'password': result[3],
                    'profile_image': result[4],
                }
                return user
            return None
    except Exception as e:
        # Manejar cualquier otro error no esperado
        print(f"Error inesperado al obtener usuario: {e}")
        return None


def update_user(user_id: int, username: str, email: str, password: str,
                profile_image: bytes) -> int:
    """
    Modifica los datos usuario en la base de datos.

    Esta función modifica un registro en la tabla 'users' con el nombre de usuario,
    correo electrónico, contraseña y la imagen de perfil proporcionados. Si la operación
    es exitosa, retorna 0. En caso de error, retorna 1.

    Args:
        user_id (int): El id del usuario.
        username (str): El nombre de usuario.
        email (str): El correo electrónico del usuario.
        password (str): La contraseña del usuario.
        profile_image (bytes): La imagen de perfil del usuario en formato binario.

    Returns:
        int: 0 si la operación es exitosa, 1 en caso de error.
    """

    # pylint: disable=broad-exception-caught

    try:
        # Iniciar una transacción.
        with db.engine.begin() as connection:
            sql = "UPDATE users SET"
            sql += " username = :username,"
            sql += " email = :email,"
            sql += " password = :password,"
            sql += " profile_image = :profile_image"
            sql += " WHERE id = :user_id;"
            values = {"username": username,
                      "email": email,
                      "password": password,
                      "profile_image": profile_image,
                      "user_id": user_id
                      }
            print(sql)
            connection.execute(text(sql), values)
            return 0
    except Exception as e:
        print(f"Error al modificar el usuario: {e}")
        return 1
