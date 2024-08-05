/**
 * Agrega validación de formularios utilizando la API Constraint Validation.
 * 
 * Este script se ejecuta cuando el contenido del DOM se ha cargado y añade un
 * manejador de eventos 'submit' a todos los formularios que tienen la clase 'needs-validation'.
 * Si un formulario no es válido, previene el envío y añade la clase 'was-validated' para
 * mostrar los mensajes de error correspondientes.
 */
(() => {
    'use strict'

    // Selecciona todos los formularios que requieren validación.
    var forms = document.querySelectorAll('.needs-validation')

    // Convierte NodeList en un array y añade manejadores de eventos a cada formulario.
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                // Si el formulario no es válido, previene el envío y la propagación del evento.
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                // Añade la clase 'was-validated' para mostrar los mensajes de error.
                form.classList.add('was-validated')
            }, false)
        })
})()
