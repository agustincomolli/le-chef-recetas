"""
Este módulo define un paso de preparación en una receta de cocina.
"""

from app import db


class Step(db.Model):
    """Modelo para representar un paso en la preparación de una receta.

    Un paso está asociado a una receta específica mediante la relación
    uno a muchos (one-to-many).

    Atributos:
        id (int): Identificador único del paso (clave primaria).
        content (str): Contenido del paso, detallando la acción a realizar 
            (requerido). Puede incluir texto multilínea.
        recipe_id (int): Identificador de la receta asociada al paso 
            (clave foránea a la tabla "recipe.id"). Este campo es obligatorio.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), 
                          nullable=False)
