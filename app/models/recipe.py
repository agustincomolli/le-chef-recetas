"""
Este módulo define una recete de cocina en la base de datos.
"""

from app import db


class Recipe(db.Model):
    """
    Modelo para representar una receta en la base de datos.

    Atributos:
        id (int): Identificador único de la receta (clave primaria).
        title (str): Título de la receta (requerido).
        description (str): Descripción opcional de la receta.
        servings (int): Cantidad de porciones que rinde la receta.
        prep_time (int): Tiempo de preparación de la receta.
        prep_time_unit (str): Unidad de tiempo para el tiempo de preparación
                              (ej. "minutos", "horas").
        cook_time (int): Tiempo de cocción de la receta.
        cook_time_unit (str): Unidad de tiempo para el tiempo de cocción (ej. "minutos", "horas").
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    servings = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    prep_time_unit = db.Column(db.String(10))
    cook_time = db.Column(db.Integer)
    cook_time_unit = db.Column(db.String(10))

    def __repr__(self) -> str:
        recipe = f"Recipe('{self.title}', '{self.servings}',"
        recipe += f"'{self.prep_time} {self.prep_time_unit}', '{
            self.cook_time} {self.cook_time_unit}')"

        return recipe
