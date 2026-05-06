from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Challenge App is running",
        "status": "ok"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": os.getenv("APP_ENV", "production")
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
