"""Simple Flask test to verify server works"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "OK", "message": "Flask is working!"})

@app.route('/api/test')
def test():
    return jsonify({"test": "success"})

if __name__ == '__main__':
    print("🧪 Testing Flask on http://localhost:5001")
    app.run(debug=True, port=5001)
