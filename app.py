from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__, static_folder="static")

# Configura tu API key de Gemini
genai.configure(api_key="GEMINI_API_KEY")

# Carga el modelo correcto (puede ser uno de los disponibles)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Opciones de estilo
niveles = {
    "sencillo": "Parafrasea el siguiente texto de forma clara y sencilla:",
    "medio": "Parafrasea el siguiente texto con un nivel intermedio, manteniendo un tono natural:",
    "formal": "Parafrasea el siguiente texto con un tono formal y profesional:",
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/parafrasear", methods=["POST"])
def parafrasear():
    texto = request.form.get("texto", "").strip()
    nivel = request.form.get("nivel", "").strip().lower()

    # Si no se selecciona nivel, usar "sencillo" por defecto
    if nivel not in niveles:
        nivel = "sencillo"

    if not texto:
        return jsonify({"resultado": "⚠️ Por favor, escribe algún texto."})

    prompt = niveles[nivel]
    mensaje = f"{prompt} \"{texto}\""

    try:
        response = model.generate_content(mensaje)
        return jsonify({"resultado": response.text.strip()})
    except Exception as e:
        return jsonify({"resultado": f"❌ Error al usar Gemini: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
