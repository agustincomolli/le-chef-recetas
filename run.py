"""
Script de ejecución para la aplicación Flask.

Este script inicializa y ejecuta la aplicación Flask. Se utiliza para
iniciar el servidor de desarrollo y puede ser configurado para diferentes
entornos (desarrollo, pruebas, producción).

"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
