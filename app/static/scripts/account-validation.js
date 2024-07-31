/**
 * Script de validación mejorado para envío de formulario
 *
 * Este script agrega validación adicional a los formularios con la clase 'needs-validation'
 * para asegurar que los datos ingresados sean correctos antes de enviar el formulario.
 *
 * La validación incluye:
 * - Validación estándar de Bootstrap
 * - Validación de coincidencia de contraseñas
 */
(() => {
  'use strict';

  // Selecciona todos los formularios con la clase 'needs-validation'
  const forms = document.querySelectorAll('.needs-validation');

  // Itera sobre cada formulario encontrado
  Array.from(forms).forEach(form => {
    // Agrega un listener para el evento 'submit' del formulario
    form.addEventListener('submit', event => {
      let formValid = true; // Inicializa la bandera de validación

      // Realiza la validación estándar de Bootstrap
      if (!form.checkValidity()) {
        formValid = false; // Si la validación falla, establece la bandera en false
      }

      // Obtiene los elementos de entrada para las contraseñas
      const password = form.querySelector('#password') || form.querySelector('#new_password');
      const confirmation = form.querySelector('#confirmation');

      // Valida la coincidencia de contraseñas solo si el campo de nueva contraseña no está vacío
      if (password && confirmation) {
        console.log(password.value);
        if (password.value.length !== '' && password.value !== confirmation.value) {
          // Si las contraseñas no coinciden, establece un mensaje de error personalizado
          confirmation.setCustomValidity('Las contraseñas no coinciden');
          formValid = false;
        } else {
          // Si las contraseñas coinciden o el campo de nueva contraseña está vacío, borra el mensaje de error
          confirmation.setCustomValidity('');
        }
      }

      // Valida el tamaño del archivo de imagen
      const imageInput = form.querySelector('#input-profile-image');
      if (imageInput && imageInput.files.length > 0) {
        const file = imageInput.files[0];
        if (file.size > 1048576) { // 1MB en bytes
          formValid = false;
          imageInput.setCustomValidity('El archivo debe ser menor de 1MB');
        } else {
          imageInput.setCustomValidity('');
        }
      }

      // Si la validación falló, previene el envío del formulario y muestra los mensajes de error
      if (!formValid) {
        event.preventDefault();
        event.stopPropagation();
      }

      // Agrega la clase 'was-validated' al formulario para mostrar los mensajes de error
      form.classList.add('was-validated');
    }, false);
  });
})();
