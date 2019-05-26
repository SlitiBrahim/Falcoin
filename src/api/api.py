from flask import Flask, jsonify

app = Flask(__name__)

def run():
    app.run(host='0.0.0.0', debug=True)

@app.route('/')
def index():
    return jsonify({'message': 'hello'})