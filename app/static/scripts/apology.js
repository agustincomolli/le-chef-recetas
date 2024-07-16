document.addEventListener('DOMContentLoaded', () => {
    // Función para cambiar el color del spinner
    function changeSpinnerColor() {
        const spinner = document.getElementById('colorful-spinner');
        const colors = ['text-primary', 'text-secondary', 'text-success', 'text-danger', 'text-warning', 'text-info', 'text-light', 'text-dark'];
        let currentColorIndex = 0;

        setInterval(() => {
            // Quitar el color actual
            spinner.classList.remove(colors[currentColorIndex]);
            // Calcular el próximo color
            currentColorIndex = (currentColorIndex + 1) % colors.length;
            // Añadir el próximo color
            spinner.classList.add(colors[currentColorIndex]);
        }, 2000);
    }

    // Llamar a la función para iniciar el cambio de colores
    changeSpinnerColor();
});