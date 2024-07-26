"""
Este módulo contiene las extensiones de Flask utilizadas en la aplicación.

Las extensiones se inicializan aquí para evitar importaciones circulares y
para mantener una estructura de código limpia y modular.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
