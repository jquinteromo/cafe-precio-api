from flask import Flask, jsonify, make_response
import json
import os
import logging

app = Flask(__name__)
 
# Enable CORS so your frontend (running on a different origin) can call the API.
# For production, replace "*" with the specific origin of your frontend (e.g. "https://mi-frontend.com").
CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route("/api/precio", methods=["GET"])
def get_precio():
    try:
        with open("precio.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        # File not found: return a 404 with a helpful message
        return make_response(jsonify({"error": "precio_not_found", "message": "El precio aún no está disponible."}), 404)
    except json.JSONDecodeError:
        # Corrupt JSON: return 500 and log the error
        logging.exception("precio.json is not valid JSON")
        return make_response(jsonify({"error": "invalid_json", "message": "El archivo precio.json está corrupto."}), 500)
    except Exception as e:
        # Any other unexpected error
        logging.exception("Unexpected error reading precio.json")
        return make_response(jsonify({"error": "internal_error", "message": str(e)}), 500)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "API de precio del café."})


if __name__ == "__main__":
    # Bind to PORT if provided by the environment (Render sets $PORT).
    port = int(os.environ.get("PORT", 5000))
    # Use 0.0.0.0 so the server is reachable from outside the container.
    app.run(host="0.0.0.0", port=port)
