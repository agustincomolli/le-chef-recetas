"""
Este módulo define el modelo de Usuario para la aplicación.
"""

from app import db


class User(db.Model):
    """
    Representa un usuario en la aplicación.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario único del usuario.
        email (str): Dirección de correo electrónico única del usuario.
        password (str): Contraseña cifrada del usuario.
        avatar (str): URL o ruta al avatar del usuario.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"
