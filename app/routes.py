"""
Contiene las rutas a cada parte de la aplicación web

"""
from flask import Blueprint
from app.helpers import apology

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    """ Página principal """
    return apology("trabajá sorete")
