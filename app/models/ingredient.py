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
        name (str): Nombre del ingrediente (máximo 50 caracteres).
        recipe_id (int): Identificador de la receta asociada al ingrediente 
            (clave foránea a la tabla "recipe.id"). Este campo es obligatorio.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
