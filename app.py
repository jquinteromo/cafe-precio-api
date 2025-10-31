from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/api/precio", methods=["GET"])
def get_precio():
    with open("precio.json") as f:
        return jsonify(json.load(f))

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "API de precio del café."})
