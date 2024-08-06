"""
Este módulo define un ingrediente en una receta.
"""

from app import db


class Ingredient(db.Model):
    """
    Modelo para representar un ingrediente en una receta.

    Un ingrediente está asociado a una receta específica mediante la relación
    uno a muchos (one-to-many).

    Atributos:
        id (int): Identificador único del ingrediente (clave primaria).
        description (str): Nombre del ingrediente (máximo 50 caracteres).
        recipe_id (int): Identificador de la receta asociada al ingrediente 
            (clave foránea a la tabla "recipes.id"). Este campo es obligatorio.
    """
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    # Clave foránea y relación con Recipe
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"),
                          nullable=False)
    recipe = db.relationship("Recipe", back_populates="recipes")
