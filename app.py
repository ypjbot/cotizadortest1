from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from google.cloud import vision

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde el frontend

# Configurar la API de Google Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\\JP\\GoogleVisionApi\\woven-honor-442102-t1-688a63442722.json"
client = vision.ImageAnnotatorClient()

# Función para evaluar la cantidad y complejidad de las figuras detectadas
def evaluar_figuras_complejas(etiquetas):
    figuras_muy_complejas = ["Symbol", "Polygon", "Curve"]
    figuras_complejas = ["Triangle", "Parallel"]
    figuras_simples = ["Circle", "Line", "Rectangle"]

    contador_muy_complejas = 0
    contador_complejas = 0
    contador_simples = 0

    for etiqueta in etiquetas:
        if any(figura in etiqueta for figura in figuras_muy_complejas):
            contador_muy_complejas += 1
        elif any(figura in etiqueta for figura in figuras_complejas):
            contador_complejas += 1
        elif any(figura in etiqueta for figura in figuras_simples):
            contador_simples += 1

    puntos_figuras = (contador_muy_complejas * 50) + (contador_complejas * 10) + (contador_simples * 2)
    return puntos_figuras

# Función para calcular el precio con las reglas dadas
def calcular_precio(puntuacion_complejidad):
    if puntuacion_complejidad < 20:
        precio = puntuacion_complejidad + 20
    elif puntuacion_complejidad < 60:
        precio = puntuacion_complejidad * 1.08
    else:
        precio = puntuacion_complejidad * 1.15
    return round(precio, 2)

# Ruta principal
@app.route('/')
def home():
    return "Bienvenido al backend del Cotizador de Bordados"

# Ruta para procesar la imagen y calcular el precio
@app.route('/procesar-imagen', methods=['POST'])
def procesar_imagen():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se ha enviado ninguna imagen"}), 400

    imagen = request.files['imagen']
    if imagen.filename == '':
        return jsonify({"error": "El archivo de imagen está vacío"}), 400

    contenido = imagen.read()
    image = vision.Image(content=contenido)

    # Obtener etiquetas de Google Vision
    respuesta_etiquetas = client.label_detection(image=image)
    etiquetas = [etiqueta.description for etiqueta in respuesta_etiquetas.label_annotations]

    # Calcular complejidad y precio
    puntuacion_complejidad = evaluar_figuras_complejas(etiquetas)
    precio = calcular_precio(puntuacion_complejidad)

    return jsonify({
        "mensaje": "Imagen procesada con éxito",
        "etiquetas": etiquetas,
        "puntuacion_complejidad": puntuacion_complejidad,
        "precio": f"{precio} MXN"
    })

if __name__ == '__main__':
    app.run(debug=True)
