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
    categories = [{"id": category[0], "name": category[1]}
                  for category in result.fetchall()]
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


def get_recipe_by_id(recipe_id: int) -> dict:
    """
    Obtiene una receta de la base de datos por su ID.

    Args:
        recipe_id (int): El ID de la receta a obtener.

    Returns:
        dict: Un diccionario con la información de la receta, o None si no se encuentra.
    """
    try:
        with db.engine.connect() as connection:
            sql = """
            SELECT r.*, c.name as category_name 
            FROM recipes r
            JOIN categories c ON r.category_id = c.id
            WHERE r.id = :recipe_id
            """
            result = connection.execute(
                text(sql), {"recipe_id": recipe_id}).fetchone()
            if result:
                recipe = dict(result)

                # Obtener ingredientes
                ingredients_sql = "SELECT description FROM ingredients WHERE recipe_id = :recipe_id"
                ingredients = connection.execute(text(ingredients_sql),
                                                 {"recipe_id": recipe_id}).fetchall()
                recipe['ingredients'] = [ing[0] for ing in ingredients]

                # Obtener pasos
                steps_sql = "SELECT description FROM steps "
                steps_sql += "WHERE recipe_id = :recipe_id ORDER BY order_num"
                steps = connection.execute(
                    text(steps_sql), {"recipe_id": recipe_id}).fetchall()
                recipe['steps'] = [step[0] for step in steps]

                return recipe
            return None
    except SQLAlchemyError as e:
        print(f"Error de base de datos al obtener receta: {e}")
        return None


def add_recipe(title: str, description: str, category_id: int, servings: int,
               prep_time: int, cook_time: int, image_filename: str,
               ingredients: list, steps: list, user_id: int) -> int:
    """
    Agrega una nueva receta a la base de datos.

    Args:
        title (str): Título de la receta.
        description (str): Descripción de la receta.
        category_id (int): ID de la categoría de la receta.
        servings (int): Número de porciones.
        prep_time (int): Tiempo de preparación en minutos.
        cook_time (int): Tiempo de cocción en minutos.
        image_filename (str): Nombre del archivo de imagen de la receta.
        ingredients (list): Lista de ingredientes.
        steps (list): Lista de pasos de preparación.
        user_id (int): ID del usuario que crea la receta.

    Returns:
        int: ID de la receta creada si es exitoso, None si hay un error.
    """
    try:
        with db.engine.begin() as connection:
            # Insertar la receta
            recipe_sql = """
            INSERT INTO recipes (title, description, category_id, servings, prep_time, cook_time, image, user_id)
            VALUES (:title, :description, :category_id, :servings, :prep_time, :cook_time, :image, :user_id)
            RETURNING id
            """
            recipe_values = {
                "title": title, "description": description, "category_id": category_id,
                "servings": servings, "prep_time": prep_time, "cook_time": cook_time,
                "image": image_filename, "user_id": user_id
            }
            result = connection.execute(text(recipe_sql), recipe_values)
            recipe_id = result.fetchone()[0]

            # Insertar ingredientes
            for ingredient in ingredients:
                ingredient_sql = "INSERT INTO ingredients (recipe_id, description) "
                ingredient_sql += "VALUES (:recipe_id, :description)"
                connection.execute(text(ingredient_sql),
                                   {"recipe_id": recipe_id, "description": ingredient})

            # Insertar pasos
            for i, step in enumerate(steps, start=1):
                step_sql = "INSERT INTO steps (recipe_id, order_num, description) "
                step_sql += "VALUES (:recipe_id, :order_num, :description)"
                connection.execute(
                    text(step_sql), {"recipe_id": recipe_id, "order_num": i, "description": step})

            return recipe_id
    except SQLAlchemyError as e:
        print(f"Error de base de datos al agregar receta: {e}")
        return None


def update_recipe(recipe_id: int, title: str, description: str, category_id: int,
                  servings: int, prep_time: int, cook_time: int, image_filename: str,
                  ingredients: list, steps: list) -> bool:
    """
    Actualiza una receta existente en la base de datos.

    Args:
        recipe_id (int): ID de la receta a actualizar.
        title (str): Nuevo título de la receta.
        description (str): Nueva descripción de la receta.
        category_id (int): Nuevo ID de la categoría de la receta.
        servings (int): Nuevo número de porciones.
        prep_time (int): Nuevo tiempo de preparación en minutos.
        cook_time (int): Nuevo tiempo de cocción en minutos.
        image_filename (str): Nuevo nombre del archivo de imagen de la receta.
        ingredients (list): Nueva lista de ingredientes.
        steps (list): Nueva lista de pasos de preparación.

    Returns:
        bool: True si la actualización es exitosa, False si hay un error.
    """
    try:
        with db.engine.begin() as connection:
            # Actualizar la receta
            recipe_sql = """
            UPDATE recipes 
            SET title = :title, description = :description, category_id = :category_id, 
                servings = :servings, prep_time = :prep_time, cook_time = :cook_time, 
                image = :image
            WHERE id = :recipe_id
            """
            recipe_values = {
                "recipe_id": recipe_id, "title": title, "description": description,
                "category_id": category_id, "servings": servings, "prep_time": prep_time,
                "cook_time": cook_time, "image": image_filename
            }
            connection.execute(text(recipe_sql), recipe_values)

            # Eliminar ingredientes y pasos existentes
            connection.execute(text("DELETE FROM ingredients WHERE recipe_id = :recipe_id"),
                               {"recipe_id": recipe_id})
            connection.execute(text("DELETE FROM steps WHERE recipe_id = :recipe_id"),
                               {"recipe_id": recipe_id})

            # Insertar nuevos ingredientes
            for ingredient in ingredients:
                ingredient_sql = "INSERT INTO ingredients (recipe_id, description) "
                ingredient_sql += "VALUES (:recipe_id, :description)"
                connection.execute(text(ingredient_sql),
                                   {"recipe_id": recipe_id, "description": ingredient})

            # Insertar nuevos pasos
            for i, step in enumerate(steps, start=1):
                step_sql = "INSERT INTO steps (recipe_id, order_num, description) "
                step_sql += "VALUES (:recipe_id, :order_num, :description)"
                connection.execute(text(step_sql),
                                   {"recipe_id": recipe_id,
                                    "order_num": i,
                                    "description": step})

            return True
    except SQLAlchemyError as e:
        print(f"Error de base de datos al actualizar receta: {e}")
        return False
