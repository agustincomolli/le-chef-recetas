document.addEventListener('DOMContentLoaded', function () {
    // Variables de referencia a los elementos del DOM
    const addIngredient = document.querySelector('#addIngredient');
    const addStep = document.querySelector('#addStep');
    const ingredientsList = document.querySelector('#ingredientsList');
    const stepsList = document.querySelector('#stepsList');
    const recipeImageElement = document.getElementById('img-recipe-image');
    const recipeImageInput = document.getElementById('input-recipe-image');
    const categorySelect = document.querySelector('select[name="category"]');
    const cancelButton = document.querySelector("#cancel-button");

    const minLines = 3; // Número mínimo de líneas en un textarea


    /**
     * Crea un nuevo elemento de entrada (input o textarea) para ingredientes o pasos.
     * @param {string} type - El tipo de elemento a crear ('ingredient' o 'step').
     * @returns {HTMLElement} - El elemento creado.
     */
    function createItemElement(type) {
        const div = document.createElement('div');
        div.className = 'input-group mb-2';

        let input;
        if (type === 'ingredient') {
            // Crear un input para ingrediente
            input = document.createElement('input');
            input.type = 'text';
            input.name = 'ingredients[]';
            input.placeholder = "p.ej. 2 tazas de harina, tamizada";
        } else {
            // Crear un textarea para paso
            const stepNumber = document.createElement("label");
            stepNumber.className = 'form-label text-start w-100';
            stepNumber.textContent = `Paso ${stepsList.children.length + 1}`;
            div.appendChild(stepNumber);
            input = document.createElement('textarea');
            input.name = 'steps[]';
            input.rows = minLines; // Establece 3 líneas de forma predeterminada
            input.placeholder = "Por ejemplo, combine todos los ingredientes secos en un tazón grande…";
        }
        input.className = 'form-control';
        input.required = true;

        // Crear botones de acción
        const removeBtn = createButton('btn-danger', 'bi-trash', 'remove-item');
        const upBtn = createButton('btn-secondary', 'bi-arrow-up', 'move-up');
        const downBtn = createButton('btn-secondary', 'bi-arrow-down', 'move-down');

        // Añadir elementos al div
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
     * Crea un botón con las clases y el ícono especificados.
     * @param {string} className - Las clases del botón.
     * @param {string} iconClass - Las clases del ícono del botón.
     * @param {string} actionClass - La clase de acción del botón.
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

    // Añadir un nuevo ingrediente al hacer clic en el botón
    addIngredient.addEventListener('click', function () {
        ingredientsList.appendChild(createItemElement('ingredient'));
    });

    // Añadir un nuevo paso al hacer clic en el botón
    addStep.addEventListener('click', function () {
        stepsList.appendChild(createItemElement('step'));
    });

    // Manejar eventos de clic en los botones de eliminar, mover arriba y mover abajo
    document.addEventListener('click', function (e) {
        if (e.target.closest('.remove-item')) {
            const itemGroup = e.target.closest('.input-group');
            if (itemGroup.parentNode.children.length > 1) {
                itemGroup.remove();
                updateStepNumbers();
            }
        } else if (e.target.closest('.move-up')) {
            const item = e.target.closest('.input-group');
            const prev = item.previousElementSibling;
            if (prev) {
                item.parentNode.insertBefore(item, prev);
            }
        } else if (e.target.closest('.move-down')) {
            const item = e.target.closest('.input-group');
            const next = item.nextElementSibling;
            if (next) {
                item.parentNode.insertBefore(next, item);
            }
        }
    });

    /**
     * Actualiza los números de los pasos después de un cambio en la lista.
     */
    function updateStepNumbers() {
        const stepLabels = document.querySelectorAll('#stepsList .form-label');
        stepLabels.forEach((label, index) => {
            label.textContent = `Paso ${index + 1}`;
        });
    }

    // Cambia la imagen de la receta según la categoría seleccionada
    categorySelect.addEventListener('change', function () {
        if (!recipeImageInput.value) {
            const selectedOption = this.options[this.selectedIndex];
            const imageUrl = selectedOption.dataset.imageUrl;
            if (imageUrl) {
                recipeImageElement.src = imageUrl;
            } else {
                recipeImageElement.src = '/static/images/others.webp';
            }
        }
    });

    // Redirigir al usuario a la página principal al hacer clic en cancelar
    cancelButton.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "/";
    });
});
