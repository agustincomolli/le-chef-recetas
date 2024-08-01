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
from app.utils.database import is_unique_username, is_unique_email
from app.utils.database import add_user, get_user, delete_user, update_user


# Códigos de error.
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
ERROR_IMAGE_TOO_BIG = "El archivo debe ser menor de 1MB"
ERROR_DB_OPERATION = 1

auth = Blueprint('auth', __name__)


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """
    Renderiza la página de la cuenta de usuario y maneja la actualización de los datos de la cuenta.

    Si el método de la solicitud es POST, procesa el formulario de actualización de la cuenta.
    Verifica la validez de los datos del formulario, comprueba la contraseña actual, actualiza
    la imagen de perfil y la información del usuario en la base de datos. Redirige a la página
    principal con un mensaje flash que indica el resultado de la operación.

    Si el método de la solicitud es GET, renderiza la plantilla de la cuenta con la información
    del usuario actual.

    Returns:
        Response: La respuesta de la solicitud, que será la plantilla "account.html" para GET 
                  o una redirección con un mensaje flash para POST.
    """
    user = get_user(session["username"])
    user["profile_image"] = session["profile_image"]

    if request.method == "POST":
        form_data = request.form

        is_valid_form, message, code = validate_profile_data(form_data,
                                                             update=True)
        # Si hay algún problema con los datos del formulario...
        if not is_valid_form:
            return apology(message, code)

        # Comprobar si la contraseña actual es correcta.
        if not check_password_hash(user["password"], form_data["current_password"]):
            flash("La contraseña actual es incorrecta", "danger")
            return redirect("/account")

        # Obtener la imagen del perfil.
        profile_image_file = request.files.get('input-profile-image')
        if profile_image_file:
            profile_image = get_profile_image(profile_image_file)
        else:
            profile_image = get_user(session["username"])["profile_image"]

        if not form_data["new_password"]:
            password = generate_password_hash(form_data["current_password"])
        else:
            password = generate_password_hash(form_data["new_password"])

        # Actualiza los datos del usuario en la base de datos
        result_update_user = update_user(session["user_id"],
                                         form_data["username"],
                                         form_data["email"],
                                         password,
                                         profile_image)
        if not result_update_user == ERROR_DB_OPERATION:
            flash('Su información ha sido actualizada con exito.', 'success')
            return redirect("/login")

        return apology("No se pudo modificar el usuario.", 500)

    return render_template("account.html", user=user)


@auth.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    """
    Elimina la cuenta del usuario actual y limpia la sesión.

    Returns:
        redirect: Redirige a la página de inicio si la eliminación es exitosa.
                  Redirige a la página de cuenta si ocurre un error.
    """

    user_id = session["user_id"]
    result = delete_user(user_id)
    if not result == ERROR_DB_OPERATION:
        # Eliminar la sesión.
        session.clear()
        # Informar al usuario.
        flash('Tu cuenta ha sido eliminada exitosamente.', 'success')
        return redirect("/")

    flash('No se pudo eliminar la cuenta. Por favor, inténtalo de nuevo.', 'danger')
    return redirect("/account")


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

        is_valid_form, message, code = validate_profile_data(form_data)
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
        if not result_add_user == ERROR_DB_OPERATION:
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect("/login")
        else:
            return apology("No se pudo agregar el usuario.", 500)

    else:
        return render_template("register.html")


def validate_profile_data(form_data: dict, update=False) -> tuple:
    """
    Valida los datos del formulario de registro o actualización de usuario.

    Args:
        form_data (dict): Los datos del formulario enviados por el usuario.
        update (bool): Indica si se trata de una actualización de usuario. 
                       Por defecto es False.

    Returns:
        tuple: Una tupla que contiene:
            - bool: True si todas las validaciones pasan, False si alguna falla.
            - str: Mensaje de error si alguna validación falla, "OK" si todas pasan.
            - int: Código de estado HTTP, 200 si todas las validaciones pasan, otro código 
                   si alguna falla.
    """
    validations = []

    # Validar la imagen de perfil
    image_file = request.files.get('input-profile-image')
    validations.append(validate_profile_image(image_file))

    # Validar el nombre de usuario
    validations.append(validate_username(form_data["username"], update))

    # Validar el correo electrónico
    validations.append(validate_email(form_data["email"], update))

    # Validaciones específicas para actualización
    if update:
        password = form_data["current_password"]
        new_password = form_data["new_password"]

        # Validar las contraseñas
        validations.append(validate_passwords(password, "", True))
        if new_password:
            confirmation = form_data["confirmation"]
            validations.append(validate_passwords(new_password, confirmation))

    # Validaciones específicas para registro
    else:
        password = form_data["password"]
        confirmation = form_data["confirmation"]

        # Validar las contraseñas
        validations.append(validate_passwords(password, confirmation))

    # Comprobar cada validación
    for validation in validations:
        is_valid, message, code = validation
        if not is_valid:
            return is_valid, message, code

    return True, "OK", 200


def validate_profile_image(image_file) -> tuple:
    """
    Valida la imagen de perfil.

    Args:
        image_file: El archivo de imagen subido.

    Returns:
        tuple: (bool, str, int) - Indica si la imagen es válida, el mensaje de error y el 
                código de estado HTTP.
    """
    if image_file and allowed_file(image_file.filename):
        if image_file.content_length > 1048576:  # 1MB en bytes
            return False, ERROR_IMAGE_TOO_BIG, 400
    return True, "", 200


def validate_username(username: str, update: bool) -> tuple:
    """
    Valida el nombre de usuario.

    Args:
        username (str): El nombre de usuario.
        update (bool): Indica si se trata de una actualización de cuenta.

    Returns:
        tuple: (bool, str, int) - Indica si el nombre de usuario es válido, el mensaje de 
               error y el código de estado HTTP.
    """
    if not username:
        return False, ERROR_MUST_PROVIDE_USERNAME, 400
    if not update and not is_unique_username(username):
        return False, ERROR_USER_EXIST, 400
    return True, "", 200


def validate_email(email: str, update: bool) -> tuple:
    """
    Valida el correo electrónico.

    Args:
        email (str): El correo electrónico.
        update (bool): Indica si se trata de una actualización de cuenta.

    Returns:
        tuple: (bool, str, int) - Indica si el correo electrónico es válido, el mensaje de 
               error y el código de estado HTTP.
    """
    if not email:
        return False, ERROR_MUST_PROVIDE_EMAIL, 400
    if not update and not is_unique_email(email):
        return False, ERROR_EMAIL_EXIST, 400
    return True, "", 200


def validate_passwords(password: str, confirmation: str, skip_confirmation: bool = False) -> tuple:
    """
    Valida las contraseñas proporcionadas y su confirmación.

    Args:
        password (str): La contraseña proporcionada.
        confirmation (str): La confirmación de la contraseña.
        skip_confirmation (bool): Indica si se debe omitir la confirmación de la contraseña. 
                                  Por defecto es False.

    Returns:
        tuple: Una tupla que contiene:
            - bool: True si la validación pasa, False si falla.
            - str: Mensaje de error si la validación falla, vacío si pasa.
            - int: Código de estado HTTP, 200 si la validación pasa, otro código si falla.
    """

    if not password:
        return False, ERROR_MUST_PROVIDE_PASSWORD, 400

    if password and (not 8 <= len(password) <= 20):
        return False, ERROR_INVALID_LENGTH_PASSWORD, 400

    if password and password != confirmation and not skip_confirmation:
        return False, ERROR_NOT_EQUAL_PASSWORD, 400

    return True, "", 200


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


def allowed_file(filename: str) -> bool:
    """
    Verifica si el nombre de archivo tiene una extensión permitida.

    Args:
        filename (str): El nombre del archivo a verificar.

    Returns:
        bool: True si el archivo tiene una extensión permitida, False en caso contrario.
    """
    # Verificar si el nombre de archivo contiene un punto (.)
    if '.' in filename:
        # Separar el nombre de archivo por el punto y verificar la extensión
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return False
