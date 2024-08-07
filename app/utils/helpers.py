"""
Funciones auxiliares.

Este módulo contiene funciones de utilidad que se usan en varias partes de la aplicación.

"""
from sys import argv
from functools import wraps
from flask import redirect, render_template, session
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def convert_to_webp(input_path, output_path=None):
    """
    Convierte una imagen en formato WebP.

    Args:
        input_path (str): Ruta de entrada de la imagen.
        output_path (str, optional): Ruta de salida donde se guardará la imagen convertida. 
            Si no se proporciona, la imagen se guarda temporalmente en 'temp.webp'.

    Returns:
        PIL.Image.Image or None: Si no se proporciona un 'output_path', retorna el objeto 
        de imagen convertido. Si se proporciona 'output_path', no retorna nada.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo en 'input_path'.
        OSError: Si ocurre un error al abrir o guardar la imagen.

    """
    try:
        image = Image.open(input_path)
        if output_path:
            image.save(output_path, 'webp')
            print(f"Imagen convertida y guardada en {output_path}")
        else:
            image.save('temp.webp', 'webp')
            return Image.open('temp.webp')
    except FileNotFoundError:
        print(f"Archivo no encontrado: {input_path}")
    except OSError as e:
        print(f"Error al abrir o guardar la imagen: {e}")


def resize_image(input_path, output_path=None, new_size=(100, 100)):
    """
    Redimensiona una imagen.

    Args:
        input_path (str): Ruta de entrada de la imagen.
        output_path (str, optional): Ruta de salida donde se guardará la imagen redimensionada. 
            Si no se proporciona, la imagen redimensionada se retorna como un objeto 
            PIL.Image.Image.
        new_size (tuple, optional): Tamaño nuevo de la imagen como una tupla (ancho, alto). 
            Por defecto es (100, 100).

    Returns:
        PIL.Image.Image or None: Si no se proporciona un 'output_path', retorna el objeto de imagen 
        redimensionada. Si se proporciona 'output_path', no retorna nada.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo en 'input_path'.
        ValueError: Si hay un problema con el valor de 'new_size'.
        OSError: Si ocurre un error al abrir o guardar la imagen.

    """
    try:
        image = Image.open(input_path)
        if output_path:
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            resized_image.save(output_path)
            print(f"Imagen redimensionada y guardada en {output_path}")
        else:
            return image.resize(new_size, Image.Resampling.LANCZOS)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {input_path}")
    except ValueError as e:
        print(f"Valor incorrecto: {e}")
    except OSError as e:
        print(f"Error al abrir o guardar la imagen: {e}")


def allowed_file(filename: str) -> bool:
    """
    Verifica si el nombre de archivo tiene una extensión permitida.

    Args:
        filename (str): El nombre del archivo a verificar.

    Returns:
        bool: True si el archivo tiene una extensión permitida, False en caso contrario.
    """
    # Verificar si el nombre de archivo contiene un punto (.)
    if '.' in filename:
        # Separar el nombre de archivo por el punto y verificar la extensión
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in ALLOWED_EXTENSIONS
    return False


if __name__ == "__main__":
    if len(argv) == 3:
        convert_to_webp(argv[1], argv[2])
        resize_image(argv[2], argv[2])
    else:
        print(""" Ejemplo de uso:
        convert_to_webp("imagen_entrada.jpg", "imagen_salida.webp")
        resize_image("imagen_entrada.jpg", "imagen_redimensionada.jpg", (800, 600))
              """)
