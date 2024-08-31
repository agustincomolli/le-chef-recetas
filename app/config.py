"""
Este módulo proporciona una clase de configuración (`Config`) para almacenar información 
confidencial como la clave secreta utilizada en aplicaciones web. También define configuraciones 
relacionadas con la gestión de sesiones.

"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Representa un objeto de configuración para diversas configuraciones de la aplicación.

    Atributos:
        SECRET_KEY (str): Una clave secreta utilizada con fines criptográficos (reemplazar con
                          una clave fuerte y generada aleatoriamente en producción).
        SESSION_PERMANENT (bool): Si las sesiones deben persistir en los reinicios del navegador
                                (establecido en False aquí).
        SESSION_TYPE (str): El tipo de mecanismo de almacenamiento de sesión que se debe utilizar 
                            ("filesystem" aquí).

    """
    database_path = os.path.join(basedir, 'data', 'recipes.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_path

    # Configuración de la base de datos
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'recipes')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Asegurarse de que la URL comience con 'postgresql://'
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
