# app.py

from flask import Flask, request, jsonify
import os
import boto3
from api_pumpkin.utils.exceptions import DoesNotExist
from api_pumpkin.service.pet_service import PetService

app = Flask(__name__)

PETS_TABLE = os.environ['PETS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    DYNAMO_DB_CLIENT = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    DYNAMO_DB_CLIENT = boto3.client('dynamodb')

app.pumking_service = PetService(client=DYNAMO_DB_CLIENT,
                                 config={'PETS_TABLE': PETS_TABLE})


@app.route('/pets', methods=['GET'])
def list_pets():
    pets = []
    for pet in app.pumking_service.get_pets():
        pets.append(
            pet.to_dict()
        )
    return jsonify(pets), 200


@app.route('/pets', methods=['POST'])
def create_pets():
    pet = app.pumking_service.insert_pet(**request.json)
    return jsonify(pet.to_dict()), 201


@app.route('/pets/<string:pet_id>', methods=['GET'])
def get_pets(pet_id):
    try:
        pet = app.pumking_service.get_pet(pet_id=pet_id)
    except DoesNotExist:
        return jsonify({'error': DoesNotExist.message}), 404

    return jsonify(pet.to_dict()), 200


@app.route('/pets/<string:pet_id>/quote', methods=['POST'])
def create_quote(pet_id):
    try:
        pet = app.pumking_service.get_pet(pet_id=pet_id)
    except DoesNotExist:
        return jsonify({'error': DoesNotExist.message}), 404

    return jsonify({'quote': pet.quote()}), 200
