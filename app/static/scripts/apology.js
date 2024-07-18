document.addEventListener('DOMContentLoaded', () => {
    // Función para cambiar el color del borde de la imagen.
    function changeBorderColor() {
        const img = document.querySelector(".img-fluid")
        const colors = ['border-primary', 'border-primary-subtle',
            'border-secondary', 'border-secondary-subtle', 'border-success',
            'border-success-subtle', 'border-danger', 'border-danger-subtle',
            'border-warning', 'border-warning-subtle', 'border-info',
            'border-info-subtle', 'border-light', 'border-light-subtle',
            'border-dark', 'border-dark-subtle', 'border-black', 'border-white'];
        let currentColorIndex = 0;

        setInterval(() => {
            // Quitar el color actual
            img.classList.remove(colors[currentColorIndex]);
            // Calcular el próximo color
            currentColorIndex = (currentColorIndex + 1) % colors.length;
            // Añadir el próximo color
            img.classList.add(colors[currentColorIndex]);
        }, 2000);
    }

    // Llamar a la función para iniciar el cambio de colores
    changeBorderColor();
});