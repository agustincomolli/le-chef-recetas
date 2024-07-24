// Ejemplo inicial de JavaScript para deshabilitar el envío de formularios si hay campos inválidos
(() => {
    'use strict' // Activa el modo estricto de JavaScript para una mejor calidad de código
  
    // Obtener todos los formularios a los que queremos aplicar estilos de validación personalizados de Bootstrap
    const forms = document.querySelectorAll('.needs-validation')
  
    // Iterar sobre cada formulario y prevenir su envío si no es válido
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        // Si el formulario no es válido
        if (!form.checkValidity()) {
          event.preventDefault() // Prevenir el envío del formulario
          event.stopPropagation() // Detener la propagación del evento
        }
  
        // Agregar la clase 'was-validated' al formulario para activar los estilos de validación de Bootstrap
        form.classList.add('was-validated')
      }, false) // false para indicar que el evento no se debe capturar en la fase de captura
    })
  })() // La función se invoca inmediatamente después de su declaración
  