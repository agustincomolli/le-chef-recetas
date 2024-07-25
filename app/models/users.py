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
        profile_image (str): Imagen de perfil del usuario.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    profile_image = db.Column(db.LargeBinary, nullable=False)

    # Relación uno a muchos con Recipe
    recipes = db.relationship("Recipe", back_populates="user", 
                              lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"
