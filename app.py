from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route("/api/precio", methods=["GET"])
def get_precio():
    with open("precio.json") as f:
        return jsonify(json.load(f))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "API de precio del café."})


if __name__ == "__main__":
    # Bind to PORT if provided by the environment (Render sets $PORT).
    port = int(os.environ.get("PORT", 5000))
    # Use 0.0.0.0 so the server is reachable from outside the container.
    app.run(host="0.0.0.0", port=port)
