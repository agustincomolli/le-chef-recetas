"""
Contiene las rutas a cada parte de la aplicación web

"""
import requests
# pylint: disable=unused-import
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.helpers import apology

main = Blueprint('main', __name__)


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
            flash(
                "Error al intentar enviar el mensaje. Por favor, inténtalo de nuevo más tarde.", "error")

        # Redirigir a la página principal después del envío.
        return redirect("/")
    else:
        # Renderizar la plantilla de contacto si el método es GET.
        return render_template("contact.html")


@main.route("/")
def index():
    """ Página principal """
    return apology("trabajando,\n por favor espere", 403)
