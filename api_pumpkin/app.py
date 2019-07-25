# app.py

from flask import Flask, request, jsonify
import os
import boto3
from api_pumpkin.models.pet import Pet, PetDog, PetCat

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


@app.route('/pets', methods=['GET'])
def list_pets():
    resp = DYNAMO_DB_CLIENT.scan(TableName=PETS_TABLE)
    pets = []
    for item in resp.get('Items'):
        pets.append(
            Pet(
                id=item.get('id').get('S'),
                name=item.get('name').get('S'),
                age=int(item.get('age').get('N')),
                breed=item.get('breed').get('S'),
                gender=item.get('gender').get('S'),
                species=item.get('species').get('S'),
                zip_code=item.get('zip_code').get('S'),
            ).to_dict()
        )

    return jsonify(pets), 200


@app.route('/pets', methods=['POST'])
def create_pets():
    if request.json.get('id') is not None:
        del request.json['id']

    pet = Pet(**request.json)
    resp = DYNAMO_DB_CLIENT.put_item(
        TableName=PETS_TABLE,
        Item={
            'id': {'S': pet.id},
            'name': {'S': pet.name},
            'age': {'N': str(pet.age)},
            'breed': {'S': pet.breed},
            'gender': {'S': pet.gender},
            'species': {'S': pet.species},
            'zip_code': {'S': pet.zip_code}
        }
    )

    return jsonify(pet.to_dict()), 201


@app.route('/pets/<string:pet_id>', methods=['GET'])
def get_pets(pet_id):
    resp = DYNAMO_DB_CLIENT.get_item(
        TableName=PETS_TABLE,
        Key={
            'id': {'S': pet_id}
        }
    )

    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Pet does not exist'}), 404

    return jsonify(
        Pet(
             id=item.get('id').get('S'),
             name=item.get('name').get('S'),
             age=int(item.get('age').get('N')),
             breed=item.get('breed').get('S'),
             gender=item.get('gender').get('S'),
             species=item.get('species').get('S'),
             zip_code=item.get('zip_code').get('S'),
        ).to_dict()
        ), 200


@app.route('/pets/<string:pet_id>/quote', methods=['POST'])
def create_quote(pet_id):
    resp = DYNAMO_DB_CLIENT.get_item(
        TableName=PETS_TABLE,
        Key={
            'id': {'S': pet_id}
        }
    )

    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Pet does not exist'}), 404

    pet_dict = {
        'id': item.get('id').get('S'),
        'name': item.get('name').get('S'),
        'age': int(item.get('age').get('N')),
        'breed': item.get('breed').get('S'),
        'gender': item.get('gender').get('S'),
        'species': item.get('species').get('S'),
        'zip_code': item.get('zip_code').get('S'),
    }

    if item.get('species').get('S') == 'dog':
        pet = PetDog(**pet_dict)
    elif item.get('species').get('S') == 'cat':
        pet = PetCat(**pet_dict)
    else:
        pet = Pet(**pet_dict)

    return jsonify({'quote': pet.quote()}), 200
