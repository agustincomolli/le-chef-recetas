/**
 * Inicializa el evento para cargar la imagen de perfil.
 *
 * Este script agrega un listener al evento DOMContentLoaded para asegurar que el DOM esté completamente
 * cargado antes de intentar acceder a los elementos. Luego, agrega un event listener al input de archivo
 * para cargar la imagen de perfil cuando el usuario seleccione una imagen.
 */
document.addEventListener("DOMContentLoaded", () => {
    const inputProfileImage = document.querySelector('#input-profile-image');
    inputProfileImage.addEventListener('change', loadImage)
})

/**
 * Carga la imagen seleccionada y la muestra en la página.
 *
 * Esta función se ejecuta cuando el usuario selecciona una imagen en el input de archivo.
 * Utiliza un FileReader para leer el contenido del archivo y establece el resultado como
 * la fuente (src) de una etiqueta img para mostrar la imagen en la página.
 *
 * @param {Event} event - El evento de cambio que se dispara al seleccionar un archivo.
 */
function loadImage(event) {
    // Crear un nuevo FileReader para leer el contenido del archivo.
    var reader = new FileReader();

    // Definir la función que se ejecutará cuando la lectura del archivo esté completa.
    reader.onload = function () {
        // Seleccionar el elemento img donde se mostrará la imagen del avatar.
        var output = document.querySelector('#img-profile-image');
        // Establecer el src del img con el resultado de la lectura del archivo.
        output.src = reader.result;
    };

    // Leer el archivo seleccionado como una URL de datos.
    reader.readAsDataURL(event.target.files[0]);
};
