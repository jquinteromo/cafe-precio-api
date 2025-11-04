from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# 🛡️ Habilita CORS para que el frontend pueda hacer fetch sin bloqueos
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/precio", methods=["GET"])
def get_precio():
    try:
        # 🌐 Fuente de datos viva: GitHub Actions actualiza este archivo cada 6 horas
        url = "https://raw.githubusercontent.com/jquinteromo/cafe-precio-api/main/precio.json"
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la respuesta no es 200
        data = response.json()
        return jsonify(data)
    except Exception as e:
        # 🧯 Fallback si GitHub falla o no responde
        return jsonify({
            "precio": "—",
            "ultima_actualizacion": "No disponible",
            "error": str(e)
        })

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "API de precio del café (proxy GitHub)."})

# 🧠 Render usa gunicorn, así que no necesitas app.run()
