"""
Contiene las rutas a cada parte de la aplicación web

"""
from math import ceil
from datetime import datetime
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from app.utils.helpers import apology, login_required, save_image, allowed_file
from app.utils.database import get_categories, get_recipe, add_recipe, update_recipe
from app.utils.database import get_recipes, delete_recipe

# Códigos de error.
ERROR_MUST_PROVIDE_TITLE = "Por favor, ingresa un título para tu receta."
ERROR_IMAGE_TOO_BIG = "El archivo debe ser menor de 1MB"
ERROR_MUST_PROVIDE_CATEGORY = "Por favor, selecciona una categoría para tu receta."
ERROR_INVALID_SERVINGS = "Por favor, ingresa un número de porciones correcto (mínimo 1)."
ERROR_MUST_PROVIDE_INGREDIENT = "Por favor, ingresa un ingrediente válido."
ERROR_MUST_PROVIDE_STEP = "Debe haber al menos un paso en la preparación.."
ERROR_DB_OPERATION = 1

# Código OK
CODE_OK = "ok"

main = Blueprint('main', __name__)


@main.route("/about")
def about():
    """
    Muestra la página de Acerca de.

    Returns:
    Renderiza la plantilla 'about.html'.
    """
    return render_template("about.html")


@main.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
@main.route("/recipe/new", methods=["GET", "POST"])
@login_required
def add_edit_recipe(recipe_id=None):
    """
    Maneja la creación y edición de recetas. Si se proporciona un recipe_id, 
    la receta correspondiente se carga para su edición. Si no, se maneja la 
    creación de una nueva receta.

    Parameters:
    recipe_id (int): El ID de la receta a editar. Si es None, se crea una nueva receta.

    Returns:
    Renderiza el formulario de receta y maneja la lógica de guardar/actualizar la receta.
    """
    if recipe_id:
        recipe = get_recipe(recipe_id)
        if recipe is None:
            flash("Receta no encontrada", "error")
            return redirect(url_for("main.index"))
    else:
        recipe = None

    categories = get_categories()

    if request.method == "POST":
        recipe_data = {
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "servings": request.form.get("servings"),
            "prep_time": request.form.get("prep_time"),
            "prep_time_unit": request.form.get("prep_time_unit"),
            "cook_time": request.form.get("cook_time"),
            "cook_time_unit": request.form.get("cook_time_unit"),
            "user_id": session["user_id"],
            "category_id": request.form.get("category")
        }

        ingredients = request.form.getlist("ingredients[]")
        steps = request.form.getlist("steps[]")

        # Validar entradas
        message, code = validate_recipe(recipe_data, ingredients, steps)
        if message != CODE_OK:
            return apology(message, code)

        if not recipe_data["title"] or not recipe_data["category_id"] \
                or not ingredients or not steps:
            flash("Por favor, complete todos los campos requeridos", "error")
            return render_template("recipe-form.html", recipe=recipe, categories=categories)

        # Procesar imagen
        image = request.files.get("image")
        if image and image.filename != '':
            # El usuario ha subido una nueva imagen
            saved_image = save_image(image)
            if saved_image:
                recipe_data["image_url"] = "/static/uploads/" + saved_image
            else:
                message = "Error al guardar la imagen. "
                message += "Asegúrate de que sea un formato válido (png, jpg, jpeg, gif)."
                flash(message, "error")
                return render_template("recipe-form.html", recipe=recipe, categories=categories)
        elif not recipe:
            # Si no se sube imagen, usar la de la categoría seleccionada
            category_id = int(request.form.get("category"))
            category = next(
                (cat for cat in categories if cat["id"] == category_id))
            if category:
                recipe_data["image_url"] = category["image_url"]
            else:
                recipe_data["image_url"] = "/static/images/others.webp"
        else:
            recipe_data["image_url"] = recipe['image_url']

        # Guardar o actualizar receta
        if recipe_id:
            result = update_recipe(recipe_id, recipe_data, ingredients, steps)
        else:
            result = add_recipe(recipe_data, ingredients, steps)

        if result == 0:
            flash("Receta guardada exitosamente!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Ocurrió un error al guardar la receta", "error")

    return render_template("recipe-form.html", recipe=recipe, categories=categories)


@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Renderiza la página de contacto y maneja el envío del formulario de contacto.

    Returns:
        Response: Si el método de la solicitud es GET, renderiza la plantilla "contact.html".
                  Si el método de la solicitud es POST, envía los datos del formulario 
                  a través de Formspree y redirige a la página principal con un mensaje 
                  flash indicando el resultado del envío.
    """
    if request.method == "POST":
        # Obtener los datos del formulario.
        data = request.form.to_dict()
        timeout_value = 5

        try:
            # Enviar los datos a través de Formspree.
            response = requests.post(
                "https://formspree.io/f/xrbzqeoe",
                data=data,
                headers={"Accept": "application/json"},
                timeout=timeout_value
            )

            # Verificar el estado de la respuesta y mostrar un mensaje flash correspondiente.
            if response.status_code == 200:
                flash("Tu mensaje se ha enviado correctamente.", "success")
            else:
                flash("Lo lamentamos, no pudimos enviar tu mensaje.", "error")
        except requests.RequestException:
            flash("Error al intentar enviar el mensaje. Por favor, inténtalo de nuevo más tarde.",
                  "error")

        # Redirigir a la página principal después del envío.
        return redirect("/")

    # Renderizar la plantilla de contacto si el método es GET.
    return render_template("contact.html")


@main.route("/delete_recipe/", methods=["POST"])
@login_required
def delete_recipe_route():
    """
    Elimina una receta específica del usuario actual.

    Args:
        No se reciben argumentos explícitos, pero se requiere que el usuario esté logueado
        y que se envíe el ID de la receta a eliminar a través del formulario.

    Returns:
        Response: Un redireccionamiento a la página de recetas del usuario con un mensaje
                  flash indicando el resultado de la operación.
    """
    user_id = session["user_id"]
    recipe_id = int(request.form.get("recipe_id"))
    result = delete_recipe(recipe_id, user_id)
    if not result == ERROR_DB_OPERATION:
        # Informar al usuario.
        flash('Tu receta ha sido eliminada exitosamente.', 'success')
        return redirect(url_for('main.my_recipes'))

    flash('No se pudo eliminar la receta. Por favor, inténtalo de nuevo.', 'danger')
    return redirect(url_for('main.my_recipes'))


@main.route("/")
@main.route("/category/<int:category_id>")
def index(category_id=None):
    """
    Renderiza la página de inicio mostrando las recetas con paginación.
    Si se proporciona un category_id, filtra las recetas por esa categoría.

    Args:
        category_id (int, optional): El ID de la categoría para filtrar las recetas.

    Returns:
        Response: Renderiza la plantilla 'index.html' con los datos de las recetas,
                  el número de página actual, el número total de páginas y la cantidad 
                  de recetas por página.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20

    recipes, total_count = get_recipes(page, per_page, category_id)
    total_pages = ceil(total_count / per_page)

    categories = get_categories()

    # Obtener el nombre de la categoría actual.
    current_category_name = None
    if category_id:
        for category in categories:
            if category["id"] == category_id:
                current_category_name = category["name"]
                break

    return render_template('index.html',
                           recipes=recipes,
                           page=page,
                           total_pages=total_pages,
                           per_page=per_page,
                           categories=categories,
                           current_category=category_id,
                           current_category_name=current_category_name)


@main.route("/my_recipes")
@login_required
def my_recipes():
    """
    Muestra las recetas del usuario actual.

    Returns:
        Response: Renderiza la plantilla 'my-recipes.html' con las recetas del usuario.
    """
    user_id = session["user_id"]
    recipes, _ = get_recipes(user_id=user_id)
    return render_template('my-recipes.html', recipes=recipes)


@main.route("/recipe/view/<int:recipe_id>")
def view_recipe(recipe_id):
    """
    Muestra los detalles de una receta específica.

    Args:
        recipe_id (int): El ID de la receta a visualizar.

    Returns:
        Response: Renderiza la plantilla 'view-recipe.html' con los detalles de la receta.
                  Si la receta no se encuentra, redirige a la página de inicio con un 
                  mensaje de error.
    """
    recipe = get_recipe(recipe_id)

    # Verificar si la receta existe
    if recipe is None:
        flash("Receta no encontrada", "error")
        return redirect(url_for("main.index"))

    # Convertir created_at a datetime si es una cadena
    if isinstance(recipe['created_at'], str):
        date_string = recipe['created_at'].split('.')[0]
        recipe['created_at'] = datetime.strptime(date_string,
                                                 '%Y-%m-%d %H:%M:%S')

    return render_template("view-recipe.html", recipe=recipe)


@main.route("/search", methods=["GET"])
def search():
    """
    Maneja la búsqueda de recetas en la aplicación.

    Obtiene los parámetros de búsqueda de la URL, como la consulta de búsqueda, 
    el número de página y la cantidad de resultados por página. Luego, utiliza 
    estos parámetros para obtener las recetas que coinciden con la búsqueda y 
    renderiza la plantilla de índice con los resultados.

    Parámetros:
        query (str): La consulta de búsqueda.
        page (int): El número de página.
        per_page (int): La cantidad de resultados por página.

    Retorna:
        Response: La plantilla de índice renderizada con los resultados de la búsqueda.
    """
    query = request.args.get("query")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    recipes, total_count = get_recipes(page, per_page, search_query=query)
    total_pages = ceil(total_count / per_page)

    return render_template('search.html',
                           recipes=recipes,
                           query=query,
                           page=page,
                           total_pages=total_pages)


def validate_recipe(recipe: dict, ingredients: list, steps: list) -> tuple:
    """
    Valida los datos de una receta, incluyendo sus ingredientes y pasos.

    Args:
        recipe (dict): Un diccionario con los datos de la receta.
        ingredients (list): Una lista con los ingredientes de la receta.
        steps (list): Una lista con los pasos de la receta.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    validations = []
    validations.append(validate_title(recipe["title"]))
    image = request.files.get("image")
    validations.append(validate_image(image))
    validations.append(validate_category(recipe["category_id"]))
    validations.append(validate_servings(recipe["servings"]))
    validations.append(validate_ingredients(ingredients))
    validations.append(validate_steps(steps))

    # Comprobar cada validación
    for validation in validations:
        message, code = validation
        if message != CODE_OK:
            return message, code

    return CODE_OK, 200


def validate_title(title: str) -> tuple:
    """
    Valida el título de una receta.

    Args:
        title (str): El título de la receta.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if not title:
        return ERROR_MUST_PROVIDE_TITLE, 400

    return CODE_OK, 200


def validate_image(image) -> tuple:
    """
    Valida la imagen de una receta.

    Args:
        image: La imagen de la receta.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if image and allowed_file(image.filename):
        if image.content_length > 1048576:  # 1MB en bytes
            return ERROR_IMAGE_TOO_BIG, 400
    return CODE_OK, 200


def validate_category(category_id: str) -> tuple:
    """
    Valida la categoría de una receta.

    Args:
        category_id (str): El ID de la categoría.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if not category_id:
        return ERROR_MUST_PROVIDE_CATEGORY, 400

    return CODE_OK, 200


def validate_servings(servings: str) -> tuple:
    """
    Valida el número de porciones de una receta.

    Args:
        servings (str): El número de porciones.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if servings and int(servings) < 1:
        return ERROR_INVALID_SERVINGS, 400

    return CODE_OK, 200


def validate_ingredients(ingredients: list) -> tuple:
    """
    Valida los ingredientes de una receta.

    Args:
        ingredients (list): Una lista de ingredientes.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if not ingredients or ingredients[0] == "":
        return ERROR_MUST_PROVIDE_INGREDIENT, 400

    return CODE_OK, 200


def validate_steps(steps: list) -> tuple:
    """
    Valida los pasos de una receta.

    Args:
        steps (list): Una lista de pasos.

    Returns:
        tuple: Un mensaje y un código de estado HTTP.
    """
    if not steps or steps[0] == "":
        return ERROR_MUST_PROVIDE_STEP, 400

    return CODE_OK, 200
