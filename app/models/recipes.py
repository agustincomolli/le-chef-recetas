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
        user_id (int): Identificador del usuario asociado a la receta (clave foránea
            de la tabla "users.id"). Este campo es obligatorio.
        category_id (int): Identificador de la categoría asociada a la receta
            (clave foránea de la tabla "categories.id"). Este campo es obligatorio.
    """
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.current_timestamp())
    image_url = db.Column(db.String(200), nullable=False)
    servings = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    prep_time_unit = db.Column(db.String(10))
    cook_time = db.Column(db.Integer)
    cook_time_unit = db.Column(db.String(10))
    # Clave foránea y relación con User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="recipes")
    # Clave foránea y relación con Category
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"),
                            nullable=False)
    category = db.relationship("Category", back_populates="categories")
    # Relación uno a muchos con Ingredient
    ingredients = db.relationship("Ingredient", back_populates="recipe",
                                  lazy="dynamic", cascade="all, delete-orphan")
    # Relación uno a muchos con Step
    steps = db.relationship("Step", back_populates="step",
                            lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        recipe = f"Recipe('{self.title}', '{self.servings}', "
        recipe += f"'{self.prep_time} {self.prep_time_unit}', "
        recipe += f"'{self.cook_time} {self.cook_time_unit}')"

        return recipe
