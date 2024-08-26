# Le Chef - Aplicación Web de Recetas

<img src="app/static/images/le-chef.webp" alt="Logo de Le Chef" width="150px">


## Descripción

Le Chef es una aplicación web de recetas que permite a los usuarios crear, compartir y descubrir deliciosas recetas de cocina. Con una interfaz intuitiva y funciones útiles, Le Chef es la plataforma perfecta para los amantes de la cocina.

## Características Principales

- **Gestión de Usuarios**: Registro, inicio de sesión y personalización de perfiles.
- **Creación de Recetas**: Los usuarios pueden agregar sus propias recetas con imágenes, ingredientes y pasos detallados.
- **Categorización**: Las recetas se organizan en categorías para una fácil navegación.
- **Búsqueda**: Potente función de búsqueda para encontrar recetas específicas.
- **Responsive Design**: Interfaz adaptable para una experiencia óptima en dispositivos móviles y de escritorio.

## Tecnologías Utilizadas

- **Backend**: Python con Flask
- **Frontend**: HTML, CSS, JavaScript
- **Base de Datos**: SQLite
- **ORM**: SQLAlchemy
- **Diseño**: Bootstrap 5
- **Autenticación**: Flask-Session

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/agustincomolli/le-chef.git
   cd le-chef
   ```

2. Crea un entorno virtual y actívalo:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno (si es necesario).

5. Inicializa la base de datos:
   ```
   flask db upgrade
   ```

6. Ejecuta la aplicación:
   ```
   python run.py
   ```

7. Abre tu navegador y visita `http://localhost:5000`.

## Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   ├── templates/
│   └── utils/
├── instance/
├── requirements.txt
├── run.py
└── README.md
```

## Uso

1. Regístrate para crear una cuenta.
2. Inicia sesión con tus credenciales.
3. Explora las recetas existentes o crea las tuyas propias.
4. Utiliza la barra de búsqueda para encontrar recetas específicas.
5. Gestiona tu perfil y tus recetas desde el panel de usuario.

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos para contribuir:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
3. Realiza tus cambios y haz commit (`git commit -m 'Add some AmazingFeature'`).
4. Push a la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Agustín Comolli - [agustincomolli@gmail.com](mailto:tu-email@example.com)

Enlace del Proyecto: [https://github.com/agustincomolli/le-chef](https://github.com/agustincomolli/le-chef)

## Demostración

Para ver la aplicación en acción, mira este video de demostración:

[Insertar enlace de YouTube aquí]

---

Desarrollado con ❤️ por Agustín Comolli