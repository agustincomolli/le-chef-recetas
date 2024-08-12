"""
Contiene las rutas a cada parte de la aplicación web

"""
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from app.utils.helpers import apology, login_required, save_image
from app.utils.database import get_categories, get_recipe, add_recipe, update_recipe

# Códigos de error.
ERROR_MUST_PROVIDE_TITLE = "Por favor, ingresa un título para tu receta."
ERROR_IMAGE_TOO_BIG = "El archivo debe ser menor de 1MB"
ERROR_MUST_PROVIDE_CATEGORY = "Por favor, selecciona una categoría para tu receta."
ERROR_INVALID_SERVINGS = "Por favor, ingresa un número de porciones correcto (mínimo 1)."
ERROR_MUST_PROVIDE_INGREDIENT = "Por favor, ingresa un ingrediente válido."
ERROR_MUST_PROVIDE_STEP = "Por favor, describe este paso de la preparación. "
ERROR_MUST_PROVIDE_STEP += "Debe haber al menos un paso."

main = Blueprint('main', __name__)


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
    else:
        # Renderizar la plantilla de contacto si el método es GET.
        return render_template("contact.html")


@main.route("/")
def index():
    """ Página principal """
    return apology("trabajando,\n por favor espere", 403)


def validate_recipe(form_data: dict) -> tuple:
    pass
