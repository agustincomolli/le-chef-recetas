/**
 * Listener para el cambio de archivo en el input de avatar.
 * 
 * Este script agrega un event listener al input de archivo con id 'input-avatar'. 
 * Cuando el usuario selecciona un archivo, se utiliza un FileReader para cargar 
 * el contenido del archivo y mostrarlo en una etiqueta img con id 'img-avatar'.
 */
document.querySelector('#input-avatar').addEventListener('change', function(event) {
    // Crear un nuevo FileReader para leer el contenido del archivo.
    var reader = new FileReader();

    // Definir la función que se ejecutará cuando la lectura del archivo esté completa.
    reader.onload = function() {
        // Seleccionar el elemento img donde se mostrará la imagen del avatar.
        var output = document.querySelector('#img-avatar');
        // Establecer el src del img con el resultado de la lectura del archivo.
        output.src = reader.result;
    };

    // Leer el archivo seleccionado como una URL de datos.
    reader.readAsDataURL(event.target.files[0]);
});
