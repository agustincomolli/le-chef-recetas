/**
 * Escucha el evento show.bs.modal del modal de confirmación de eliminación de receta.
 * Al dispararse, extrae el id de la receta del botón que lanzó el modal y lo asigna
 * al input hidden del formulario de eliminación de receta.
 */
document.addEventListener('DOMContentLoaded', function () {
    const deleteRecipeModal = document.getElementById('deleteRecipeModal');

    deleteRecipeModal.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget;
      const recipeId = button.getAttribute('data-recipe-id');
      const form = document.getElementById('delete-recipe-form');
      const recipeIdInput = form.querySelector('input[name="recipe_id"]');
      recipeIdInput.value = recipeId;
    });
});
