"""
Este módulo contiene las funciones que tocarán la base de datos.
"""

from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app import db


def insert_categories() -> None:
    """
    Crea las categorías iniciales en la base de datos.

    Returns:
        None
    """
    categories = [{"name": "Bebidas",
                  "image_url": "/static/images/drink.webp"},
                  {"name": "Entradas",
                   "image_url": "/static/images/starter-dish.webp"},
                  {"name": "Platos principales",
                   "image_url": "/static/images/main-dish.webp"},
                  {"name": "Postres",
                   "image_url": "/static/images/dessert.webp"},
                  {"name": "Otros",
                   "image_url": "/static/images/others.webp"}]
    # Iniciar una transacción.
    with db.engine.begin() as connection:
        # Si hay categorías, salir de la función.
        if connection.execute(text("SELECT COUNT(*) FROM categories")).scalar():
            return

        for category in categories:
            category_sql = "INSERT INTO categories (name, image_url) "
            category_sql += "VALUES (:name, :image_url);"
            connection.execute(text(category_sql),
                               {"name": category["name"],
                                "image_url": category["image_url"]})
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
    categories = [{"id": category[0], "name": category[1], "image_url": category[2]}
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
            connection.execute(text(sql), values)
            return 0
    except Exception as e:
        print(f"Error al modificar el usuario: {e}")
        return 1


def get_recipe(recipe_id: int) -> dict:
    """
    Obtiene una receta de la base de datos, incluyendo sus ingredientes y pasos.

    Parameters:
    recipe_id (int): El ID de la receta a obtener.

    Returns:
    dict: Un diccionario que contiene la información de la receta, sus ingredientes y pasos.
          Devuelve None si la receta no se encuentra o si ocurre un error de base de datos.
    """
    try:
        with db.engine.connect() as conn:
            # Consultar la receta y su categoría
            query = text(
                """
                SELECT r.*, c.name as category_name 
                FROM recipes r
                JOIN categories c ON r.category_id = c.id
                WHERE r.id = :recipe_id;
                """)
            result = conn.execute(query, {"recipe_id": recipe_id}).fetchone()

            if result:
                # Convertir el resultado a un diccionario
                recipe = result._asdict()

                # Consultar los ingredientes de la receta
                ingredients_sql = "SELECT description FROM ingredients "
                ingredients_sql += "WHERE recipe_id = :recipe_id;"
                ingredients = conn.execute(text(ingredients_sql),
                                           {"recipe_id": recipe_id}).fetchall()
                recipe['ingredients'] = [ing[0] for ing in ingredients]

                # Consultar los pasos de la receta
                steps_sql = "SELECT description FROM steps "
                steps_sql += "WHERE recipe_id = :recipe_id ORDER BY order_num;"
                steps = conn.execute(text(steps_sql),
                                     {"recipe_id": recipe_id}).fetchall()
                recipe['steps'] = [step[0] for step in steps]

                return recipe
            return None
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
        return None


def add_recipe(recipe_data: dict, ingredients: list, steps: list) -> int:
    """
    Agrega una nueva receta a la base de datos.

    Parameters:
    recipe_data (dict): Un diccionario que contiene los datos de la receta.
                        Debe incluir las claves 'title', 'description', 'image_url', 'servings',
                        'prep_time', 'prep_time_unit', 'cook_time', 'cook_time_unit', 'user_id' 
                        y 'category_id'.
    ingredients (list): Una lista de descripciones de ingredientes.
    steps (list): Una lista de descripciones de los pasos para la receta.

    Returns:
    int: 0 si la operación es exitosa, 1 si hay un error.
    """
    try:
        # Iniciar una transacción.
        with db.engine.begin() as conn:
            # Añadir la fecha de creación actual
            recipe_data['created_at'] = datetime.now(timezone.utc)

            # Insertar la receta en la base de datos y obtener el ID de la receta.
            recipe_query = text(
                """
                INSERT INTO recipes (title, description, image_url, servings, prep_time, 
                prep_time_unit, cook_time, cook_time_unit, user_id, category_id, created_at)
                VALUES (:title, :description, :image_url, :servings, :prep_time, 
                :prep_time_unit, :cook_time, :cook_time_unit, :user_id, :category_id, :created_at)
                RETURNING id
                """)
            result = conn.execute(recipe_query, recipe_data)
            recipe_id = result.fetchone()[0]

            # Insertar los ingredientes en la base de datos.
            for ingredient in ingredients:
                ingredient_sql = "INSERT INTO ingredients (description, recipe_id) "
                ingredient_sql += "VALUES (:description, :recipe_id);"
                conn.execute(text(ingredient_sql),
                             {"description": ingredient, "recipe_id": recipe_id})

            # Insertar los pasos en la base de datos, manteniendo el orden.
            for i, step in enumerate(steps, 1):
                step_sql = "INSERT INTO steps (description, order_num, recipe_id) "
                step_sql += "VALUES (:description, :order_num, :recipe_id);"
                conn.execute(text(step_sql),
                             {"description": step, "order_num": i, "recipe_id": recipe_id})

        return 0
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
        return 1


def update_recipe(recipe_id: int, recipe_data: dict, ingredients: list, steps: list) -> int:
    """
    Actualiza una receta existente en la base de datos.

    Parameters:
    recipe_id (int): El ID de la receta a actualizar.
    recipe_data (dict): Un diccionario que contiene los datos actualizados de la receta.
                        Debe incluir las claves 'title', 'description', 'image_url', 'servings',
                        'prep_time', 'prep_time_unit', 'cook_time', 'cook_time_unit', 'user_id' 
                        y 'category_id'.
    ingredients (list): Una lista de descripciones de los ingredientes actualizados.
    steps (list): Una lista de descripciones de los pasos actualizados.

    Returns:
    int: 0 si la operación es exitosa, 1 si hay un error.
    """
    try:
        # Iniciar una transacción.
        with db.engine.begin() as conn:
            # Actualizar la receta en la base de datos.
            recipe_query = text(
                """
                UPDATE recipes 
                SET title = :title, description = :description, image_url = :image_url, 
                    servings = :servings, prep_time = :prep_time, prep_time_unit = :prep_time_unit, 
                    cook_time = :cook_time, cook_time_unit = :cook_time_unit, 
                    category_id = :category_id
                WHERE id = :recipe_id AND user_id = :user_id
                """)
            # Agregar el ID de la receta al diccionario de datos.
            recipe_data['recipe_id'] = recipe_id
            conn.execute(recipe_query, recipe_data)

            # Eliminar los ingredientes y pasos antiguos de la base de datos.
            conn.execute(text("DELETE FROM ingredients WHERE recipe_id = :recipe_id"), {
                         "recipe_id": recipe_id})
            conn.execute(text("DELETE FROM steps WHERE recipe_id = :recipe_id"), {
                         "recipe_id": recipe_id})

            # Insertar los nuevos ingredientes en la base de datos.
            for ingredient in ingredients:
                ingredient_sql = "INSERT INTO ingredients (description, recipe_id) "
                ingredient_sql += "VALUES (:description, :recipe_id);"
                conn.execute(text(ingredient_sql),
                             {"description": ingredient, "recipe_id": recipe_id})

            # Insertar los nuevos pasos en la base de datos, manteniendo el orden.
            for i, step in enumerate(steps, 1):
                step_sql = "INSERT INTO steps (description, order_num, recipe_id) "
                step_sql += "VALUES (:description, :order_num, :recipe_id);"
                conn.execute(text(step_sql),
                             {"description": step,
                              "order_num": i,
                              "recipe_id": recipe_id})

        return 0
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
        return 1


def get_recipes(page: int = 1, per_page: int = 20, category_id: int = None) -> tuple:
    """
    Obtiene las recetas de la base de datos, con paginación y opción de filtrar por categoría.

    Args:
        page (int): Número de página actual. Por defecto es 1.
        per_page (int): Cantidad de recetas por página. Por defecto es 20.
        category_id (int): ID de la categoría para filtrar. Si es None, se obtienen todas 
        las recetas.

    Returns:
        tuple: Una tupla que contiene:
            - list: Una lista de diccionarios con las recetas.
            - int: El número total de recetas.
    """
    # Calcular el desplazamiento para la paginación
    offset = (page - 1) * per_page

    # Consulta SQL base para obtener las recetas
    recipes_sql = """
    SELECT r.id, r.title, r.description, r.image_url, r.created_at, c.name as category_name
    FROM recipes r
    JOIN categories c ON r.category_id = c.id
    """

    # Agregar condición de filtrado por categoría si se proporciona
    if category_id is not None:
        recipes_sql += " WHERE r.category_id = :category_id"

    recipes_sql += """
    ORDER BY r.created_at DESC
    LIMIT :limit OFFSET :offset;
    """

    # Consulta SQL para obtener el número total de recetas
    count_sql = "SELECT COUNT(*) FROM recipes"
    if category_id is not None:
        count_sql += " WHERE category_id = :category_id"

    with db.engine.connect() as conn:
        # Preparar los parámetros para la consulta
        params = {"limit": per_page, "offset": offset}
        if category_id is not None:
            params["category_id"] = category_id

        # Ejecutar la consulta para obtener las recetas
        result = conn.execute(text(recipes_sql), params)
        # Convertir los resultados en una lista de diccionarios
        recipes = [row._asdict() for row in result]

        # Ejecutar la consulta para obtener el número total de recetas
        params = {}
        if category_id:
            params['category_id'] = category_id
        total_count = conn.execute(text(count_sql), params).scalar()
    return recipes, total_count
