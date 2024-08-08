document.addEventListener('DOMContentLoaded', function () {
    const addIngredient = document.querySelector('#addIngredient');
    const addStep = document.querySelector('#addStep');
    const ingredientsList = document.querySelector('#ingredientsList');
    const stepsList = document.querySelector('#stepsList');
    const recipeImageElement = document.getElementById('img-recipe-image');
    const recipeImageInput = document.getElementById('input-recipe-image');
    const categorySelect = document.querySelector('select[name="category"]');
    const cancelButton = document.querySelector("#cancel-button");

    /**
     * Crea un elemento de ingrediente o paso.
     * @param {string} type - El tipo de elemento a crear ('ingredient' o 'step').
     * @returns {HTMLElement} - El elemento de grupo de entrada creado.
     */
    function createItemElement(type) {
        const div = document.createElement('div');
        div.className = 'input-group mb-2';

        let input;
        if (type === 'ingredient') {
            input = document.createElement('input');
            input.type = 'text';
            input.name = 'ingredients[]';
            input.placeholder = "p.ej. 2 tazas de harina, tamizada";
        } else {
            const stepNumber = document.createElement("label");
            stepNumber.className = 'form-label text-start w-100';
            stepNumber.textContent = `Paso ${stepsList.children.length + 1}`;
            div.appendChild(stepNumber);
            input = document.createElement('textarea');
            input.name = 'steps[]';
            input.placeholder = "Por ejemplo, combine todos los ingredientes secos en un tazón grande…"
        }
        input.className = 'form-control';
        input.required = true;

        // Crear botones de acción
        const removeBtn = createButton('btn-danger', 'bi-trash', 'remove-item');
        const upBtn = createButton('btn-secondary', 'bi-arrow-up', 'move-up');
        const downBtn = createButton('btn-secondary', 'bi-arrow-down', 'move-down');

        // Añadir input y botones al div
        div.appendChild(input);
        div.appendChild(removeBtn);
        if (type === "step") {
            removeBtn.classList.add("ms-2");
            removeBtn.classList.add("my-auto");
        } else {
            div.appendChild(upBtn);
            div.appendChild(downBtn);
        }

        return div;
    }

    /**
     * Crea un botón con un ícono.
     * @param {string} className - Clase CSS del botón.
     * @param {string} iconClass - Clase CSS del ícono.
     * @param {string} actionClass - Clase CSS adicional para la acción.
     * @returns {HTMLElement} - El botón creado.
     */
    function createButton(className, iconClass, actionClass) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `btn ${className} ${actionClass}`;
        const icon = document.createElement('i');
        icon.className = `bi ${iconClass}`;
        button.appendChild(icon);
        return button;
    }

    // Event listener para añadir ingredientes
    addIngredient.addEventListener('click', function () {
        ingredientsList.appendChild(createItemElement('ingredient'));
    });

    // Event listener para añadir pasos de preparación
    addStep.addEventListener('click', function () {
        stepsList.appendChild(createItemElement('step'));
    });

    // Delegación de eventos para eliminar, mover hacia arriba y mover hacia abajo
    document.addEventListener('click', function (e) {
        if (e.target.closest('.remove-item')) {
            // Eliminar elemento
            const itemGroup = e.target.closest('.input-group');
            if (itemGroup.parentNode.children.length > 1) {
                // Si hay más de un elemento, eliminar el seleccionado
                itemGroup.remove();
                // Actualizar los números de los pasos
                updateStepNumbers();
            }
        } else if (e.target.closest('.move-up')) {
            // Mover elemento hacia arriba
            const item = e.target.closest('.input-group');
            const prev = item.previousElementSibling;
            if (prev) {
                item.parentNode.insertBefore(item, prev);
            }
        } else if (e.target.closest('.move-down')) {
            // Mover elemento hacia abajo
            const item = e.target.closest('.input-group');
            const next = item.nextElementSibling;
            if (next) {
                item.parentNode.insertBefore(next, item);
            }
        }
    });

    /**
     * @function updateStepNumbers
     * @description Actualiza los números de paso en la lista de pasos.
     */
    function updateStepNumbers() {
        // Selecciona todos los elementos 'form-label' de los pasos de las recetas
        const stepLabels = document.querySelectorAll('#stepsList .form-label');

        // Itera sobre cada etiqueta de paso y actualiza su contenido de texto
        stepLabels.forEach((label, index) => {
            // Actualiza el contenido de texto de la etiqueta con el número de paso correspondiente
            label.textContent = `Paso ${index + 1}`;
        });
    };

    /**
     * @event change
     * @description Escucha los cambios en la selección de categoría y actualiza la imagen 
     *              de la receta si no se ha cargado una imagen.
     */
    categorySelect.addEventListener('change', function () {
        // Verificar si se ha cargado una imagen
        if (!recipeImageInput.value) {
            // Obtener la opción seleccionada
            const selectedOption = this.options[this.selectedIndex];
            // Obtener la URL de la imagen de los datos de la opción seleccionada
            const imageUrl = selectedOption.dataset.imageUrl;
            // Actualizar el elemento de la imagen de la receta con la URL de la imagen 
            // o una imagen predeterminada
            if (imageUrl) {
                recipeImageElement.src = imageUrl;
            } else {
                recipeImageElement.src = '/static/images/others.webp';
            }
        }
    });

    /**
     * @event click
     * @description Redirige al usuario a la página de inicio cuando se hace clic 
     *              en el botón de cancelar.
     */
    cancelButton.addEventListener("click", function () {
        window.location.href = "/";
    });
});
