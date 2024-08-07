"""
Este módulo define un ingrediente en una receta.
"""

from app import db


class Category(db.Model):
    """
    Modelo para representar una categoría en la base de datos.

    Attributes:
        id (int): Identificador único de la categoría.
        name (str): Nombre de la categoría.
        image_url (str): url de la imagen de la categoría.

    Methods:
        __repr__(): Representación legible de la instancia de categoría.

    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    # Relación uno a muchos con Recipe.
    recipes = db.relationship("Recipe", back_populates="category",
                              lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Category('{self.name}')"
