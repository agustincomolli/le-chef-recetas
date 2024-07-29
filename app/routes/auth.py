"""
Este módulo se encarga de manejar las rutas relacionadas con la autenticación de usuarios,
incluyendo el inicio de sesión, cierre de sesión y registro.

"""
import tempfile
import os
import base64
from flask import Blueprint, request, redirect, render_template, session, flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.helpers import apology, convert_to_webp, resize_image, login_required
from app.utils.database import add_user, get_user, is_unique_username, is_unique_email


# Error codes.
ERROR_MUST_PROVIDE_USERNAME = "Ingresa tu nombre de usuario"
ERROR_MUST_PROVIDE_EMAIL = "Ingresa un correo electrónico válido"
ERROR_MUST_PROVIDE_PASSWORD = "Ingresa tu contraseña"
ERROR_INVALID_LENGTH_PASSWORD = "Su contraseña debe tener entre 8 y 20 caracteres"
ERROR_MUST_REPEAT_PASSWORD = "Debes repetir la contraseña"
ERROR_NOT_EQUAL_PASSWORD = "Ambas contraseñas deben ser iguales"
ERROR_USER_EXIST = "El usuario ya existe"
ERROR_USER_NOT_EXIST = "El usuario no existe"
ERROR_INCORRECT_PASSWORD = "La contraseña es incorrecta"
ERROR_EMAIL_EXIST = "El correo electrónico ya existe"
ERROR_ADD_USER = 1

auth = Blueprint('auth', __name__)


@auth.route("/account")
@login_required
def account():
    user = get_user(session["username"])
    user["profile_image"] = session["profile_image"]
    if request.method == "POST":
        pass
    else:
        return render_template("account.html", user=user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Gestiona las solicitudes de inicio de sesión (GET y POST).

    En solicitudes GET:
        - Muestra el formulario de inicio de sesión.

    En solicitudes POST:
        - Valida las credenciales del usuario (nombre de usuario y contraseña).
        - Si son válidas, inicia sesión al usuario estableciendo una variable de sesión.
        - Si son inválidas, muestra un mensaje de error.

    Returns:
        - La plantilla del formulario de inicio de sesión (GET)
        - Una redirección a una página designada después del inicio de sesión exitoso (POST)
        - Un mensaje de error (POST) si el inicio de sesión falla
    """
    # Cerrar cualquier sesión de usuario que pueda estar abierta.
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Comprobar que se proporcionó un usuario.
        if not username:
            return apology(ERROR_MUST_PROVIDE_USERNAME, 403)
        # Comprobar que se proporcionó una contraseña.
        if not password:
            return apology(ERROR_MUST_PROVIDE_PASSWORD, 403)

        user = get_user(username)
        # Comprobar si el usuario es correcto.
        if not user:
            flash(ERROR_USER_NOT_EXIST, "warning")
            return render_template("login.html")
        # Comprobar la contraseña.
        if not check_password_hash(user["password"], password):
            flash(ERROR_INCORRECT_PASSWORD, "warning")
            return render_template("login.html")

        # Guardar datos del usuario.
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        image_blob = user["profile_image"]
        # Convertir el BLOB a una cadena base64 para poder incrustarse en el html.
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        session["profile_image"] = image_base64

        # Redirigir al usuario a la página principal.
        return redirect("/")
    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    """
    Gestiona las solicitudes de cierre de sesión.

    Elimina la variable de sesión del usuario para cerrarlo de sesión.
    Redirecciona al usuario a una página designada después del cierre de sesión.

    Returns:
        - Una redirección a una página designada después del cierre de sesión exitoso
    """
    # Cerrar la sesión del usuario.
    session.clear()
    # Redirigir al usuario a la página de inicio.
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Gestiona las solicitudes de registro de usuarios (GET y POST).

    En solicitudes GET:
        - Muestra el formulario de registro.

    En solicitudes POST:
        - Valida los datos de registro del usuario (nombre de usuario, contraseña, etc.).
        - Hashea la contraseña antes de almacenarla de forma segura.
        - Crea una nueva cuenta de usuario si la validación es exitosa.
        - Si la validación falla, muestra un mensaje de error.

    Returns:
        - La plantilla del formulario de registro (GET)
        - Una redirección a una página designada después del registro exitoso (POST)
        - Un mensaje de error (POST) si el registro falla
    """
    # Código de la función register aquí
    if request.method == "POST":
        form_data = request.form

        is_valid_form, message, code = check_register_form(form_data)
        # Si hay algún problema con los datos del formulario...
        if not is_valid_form:
            return apology(message, code)

        # Guardar la contraseña en formato hash.
        hash_password = generate_password_hash(form_data["password"])
        # Obtener la imagen del perfil.
        profile_image_file = request.files.get('input-profile-image')
        profile_image = get_profile_image(profile_image_file)
        # Agregar el usuario a la base de datos
        result_add_user = add_user(form_data["username"],
                                   form_data["email"],
                                   hash_password,
                                   profile_image)
        if result_add_user == 0:
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect("/")
        else:
            return apology("No se pudo agregar el usuario.")

    else:
        return render_template("register.html")


def check_register_form(form_data: dict) -> tuple:
    """
    Valida los datos del formulario de registro de usuario.

    Esta función verifica los datos del formulario para asegurar que todos los campos 
    requeridos estén presentes y que cumplan con las condiciones necesarias. Retorna 
    una tupla que indica si los datos son válidos, un mensaje de error o éxito, y un 
    código de estado HTTP.

    Args:
        form_data (dict): Un diccionario que contiene los datos del formulario. 
            Debe incluir las claves 'username', 'email', 'password', y 'confirmation'.

    Returns:
        tuple: Una tupla que contiene un booleano indicando si los datos son válidos, 
        un mensaje de error o éxito, y un código de estado HTTP.

    Raises:
        KeyError: Si alguna de las claves esperadas no está presente en form_data.
    """
    if not form_data["username"]:
        return False, ERROR_MUST_PROVIDE_USERNAME, 400
    if not form_data["email"]:
        return False, ERROR_MUST_PROVIDE_EMAIL, 400
    if not form_data["password"]:
        return False, ERROR_MUST_PROVIDE_PASSWORD, 400
    if not len(form_data["password"]) >= 8 and len(form_data["password"]) <= 20:
        return False, ERROR_INVALID_LENGTH_PASSWORD, 400
    if not form_data["confirmation"]:
        return False, ERROR_MUST_REPEAT_PASSWORD, 400
    if not form_data["password"] == form_data["confirmation"]:
        return False, ERROR_NOT_EQUAL_PASSWORD, 400
    if not is_unique_username(form_data["username"]):
        return False, ERROR_USER_EXIST, 400
    if not is_unique_email(form_data["email"]):
        return False, ERROR_EMAIL_EXIST, 400

    return True, "OK", 200


def get_profile_image(profile_image) -> bytes:
    """
    Obtiene y procesa la imagen de perfil del usuario.

    Esta función verifica si se ha proporcionado una imagen de perfil. Si no se 
    proporciona, utiliza una imagen predeterminada. Si se proporciona una imagen, 
    la convierte al formato WebP, la redimensiona, y la retorna en formato binario.

    Args:
        profile_image: La imagen de perfil subida por el usuario. Puede ser None.

    Returns:
        bytes: La imagen de perfil procesada en formato binario.
    """
    processed_image = None

    if not profile_image or not profile_image.filename:
        # Usar la imagen predeterminada
        default_image_path = os.path.join(current_app.root_path,
                                          'static', 'images', 'chef-default.webp')
        with open(default_image_path, 'rb') as img_file:
            processed_image = img_file.read()
    else:
        # Procesamiento de la imagen subida por el usuario
        temp_original = tempfile.NamedTemporaryFile(delete=False,
                                                    suffix='.webp')
        temp_processed = tempfile.NamedTemporaryFile(delete=False,
                                                     suffix='.webp')

        try:
            profile_image.save(temp_original.name)
            convert_to_webp(temp_original.name, temp_processed.name)
            resize_image(temp_processed.name, temp_processed.name)

            with open(temp_processed.name, 'rb') as img_file:
                processed_image = img_file.read()
        finally:
            # Cerrar los archivos temporales antes de eliminarlos
            temp_original.close()
            temp_processed.close()
            # Eliminar los archivos temporales
            os.unlink(temp_original.name)
            os.unlink(temp_processed.name)

    return processed_image
