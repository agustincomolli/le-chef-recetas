"""
Contiene las rutas a cada parte de la aplicación web

"""
from flask import Blueprint, render_template, request, redirect, url_for
from app.helpers import apology
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    """ Página principal """
    return apology("trabajando,\n por favor espere", 403)
