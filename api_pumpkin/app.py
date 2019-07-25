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
