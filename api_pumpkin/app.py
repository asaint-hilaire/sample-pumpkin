# app.py

from flask import Flask
app = Flask(__name__)


@app.route('/pets', methods=['GET'])
def list_pets():
    return "Testing list!!!!"


@app.route('/pets', methods=['POST'])
def create_pets():
    return "Testing pet post!!!!"


@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pets(pet_id):
    return "Testing get pet document!!!!"


@app.route('/quote', methods=['POST'])
def create_quote():
    return "Testing quote post!!!!"
