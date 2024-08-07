/**
 * Inicializa el evento para cargar imágenes.
 *
 * Este script agrega un listener al evento DOMContentLoaded para asegurar que el DOM esté completamente
 * cargado antes de intentar acceder a los elementos. Luego, agrega un event listener a los inputs de archivo
 * para cargar imágenes cuando el usuario seleccione una imagen.
 */
document.addEventListener("DOMContentLoaded", () => {
    const profileImageInput = document.querySelector('#input-profile-image');
    const recipeImageInput = document.querySelector('#input-recipe-image');

    if (profileImageInput) {
        profileImageInput.addEventListener('change', (event) => loadImage(event, '#img-profile-image'));
    }

    if (recipeImageInput) {
        recipeImageInput.addEventListener('change', (event) => loadImage(event, '#img-recipe-image'));
    }
});

/**
 * Carga la imagen seleccionada y la muestra en la página.
 *
 * Esta función se ejecuta cuando el usuario selecciona una imagen en el input de archivo.
 * Utiliza un FileReader para leer el contenido del archivo y establece el resultado como
 * la fuente (src) de una etiqueta img para mostrar la imagen en la página.
 *
 * @param {Event} event - El evento de cambio que se dispara al seleccionar un archivo.
 * @param {string} imgSelector - El selector CSS del elemento img donde se mostrará la imagen.
 */
function loadImage(event, imgSelector) {
    // Crear un nuevo FileReader para leer el contenido del archivo.
    var reader = new FileReader();

    // Definir la función que se ejecutará cuando la lectura del archivo esté completa.
    reader.onload = function () {
        // Seleccionar el elemento img donde se mostrará la imagen.
        var output = document.querySelector(imgSelector);
        
        // Comprobar que el elemento img exista antes de asignar el src
        if (output) {
            // Establecer el src del img con el resultado de la lectura del archivo.
            output.src = reader.result;
        }
    };

    // Leer el archivo seleccionado como una URL de datos.
    reader.readAsDataURL(event.target.files[0]);
};