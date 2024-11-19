// Función para enviar la imagen al backend
function enviarImagen() {
    // Obtener el archivo de imagen desde el input
    var formData = new FormData();
    var imagen = document.getElementById('imagen').files[0];  // El input tiene el id="imagen"
    formData.append("imagen", imagen);

    // Realizar la solicitud POST al servidor Flask
    fetch('http://127.0.0.1:5000/procesar-imagen', {  // Asegúrate de que esta URL sea la correcta para tu entorno
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Manejar los datos de la respuesta del backend
        console.log(data);  // Ver la respuesta en la consola del navegador (opcional)

        // Mostrar los resultados en la página
        const resultadosDiv = document.getElementById('resultados');
        resultadosDiv.innerHTML = `
            <p><strong>Etiquetas detectadas:</strong> ${data.etiquetas.join(', ')}</p>
            <p><strong>Puntuación de complejidad:</strong> ${data.puntuacion_complejidad}</p>
            <p><strong>Precio:</strong> ${data.precio}</p>
        `;
    })
    .catch(error => {
        // Manejar cualquier error
        console.error('Error al procesar la imagen:', error);
    });
}
