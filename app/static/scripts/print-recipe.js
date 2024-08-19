// Función para imprimir la receta
function printRecipe() {
    console.log('Función printRecipe() llamada');

    // Obtener el contenido de la receta
    const recipeContent = document.querySelector('article');

    if (!recipeContent) {
        console.error('No se encontró el elemento article');
        return;
    }

    console.log('Contenido de la receta encontrado');

    // Crear una nueva ventana
    const printWindow = window.open('', '_blank');

    // Escribir el contenido HTML en la nueva ventana
    printWindow.document.write(`
        <html>
        <head>
            <title>Imprimir Receta</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.5;
                    color: #333;
                    font-size: 14px;
                    background-color: #f9f9f9;
                }
                .print-container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #2c3e50;
                    font-size: 24px;
                    margin-bottom: 20px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #34495e;
                    font-size: 18px;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                p {
                    margin: 0 0 10px;
                }
                img {
                    max-width: 100%;
                    height: auto;
                    margin-bottom: 20px;
                }
                ul, ol {
                    margin: 0 0 20px 20px;
                    padding: 0;
                }
                li {
                    margin-bottom: 5px;
                }
                .meta-info {
                    font-size: 12px;
                    color: #7f8c8d;
                    margin-bottom: 20px;
                }
                .section {
                    margin-bottom: 30px;
                }
                @media print {
                    body {
                        background-color: #fff;
                    }
                    .print-container {
                        box-shadow: none;
                    }
                    #print-recipe, .no-print {
                        display: none;
                    }
                }
            </style>
        </head>
        <body>
            <div class="print-container">
                ${recipeContent.innerHTML}
            </div>
        </body>
        </html>
    `);

    // Cerrar el documento
    printWindow.document.close();

    // Esperar a que se cargue el contenido antes de imprimir
    printWindow.onload = function () {
        // Remover elementos innecesarios
        const elementsToRemove = printWindow.document.querySelectorAll('.no-print, #print-recipe');
        elementsToRemove.forEach(el => el.remove());

        // Ajustar la estructura si es necesario
        const title = printWindow.document.querySelector('h1');
        if (title) {
            const metaInfo = printWindow.document.createElement('div');
            metaInfo.className = 'meta-info';

            // Encontrar el texto deseado
            const createdByText = Array.from(printWindow.document.querySelectorAll('p')).find(p => p.textContent.includes('Creada por:'));
            const creationDateText = Array.from(printWindow.document.querySelectorAll('p')).find(p => p.textContent.includes('Fecha de creación:'));

            if (createdByText && creationDateText) {
                metaInfo.innerHTML = `
                    <p>Creada por: ${createdByText.textContent.split(':')[1].trim()}</p>
                    <p>Fecha de creación: ${creationDateText.textContent.split(':')[1].trim()}</p>
                `;
                title.after(metaInfo);
            } else {
                console.error('No se encontraron los elementos con la información meta');
            }
        }

        printWindow.print();
        printWindow.close();
    };
}

// Agregar el evento de clic al botón de imprimir cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM cargado, buscando botón de imprimir');
    const printButton = document.querySelector('#print-recipe');
    if (printButton) {
        console.log('Botón de imprimir encontrado, agregando evento de clic');
        printButton.addEventListener('click', printRecipe);
    } else {
        console.error('No se encontró el botón de imprimir');
    }
});
