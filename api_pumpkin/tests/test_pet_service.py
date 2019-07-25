from api_pumpkin.models.pet import Pet, PetCat, PetDog
from api_pumpkin.service.pet_service import PetService
from api_pumpkin.utils.exceptions import DoesNotExist
import unittest


class MockClient(object):
    def get_item(self, **kwargs):
        if kwargs.get('TableName') is None or \
         kwargs.get('TableName').strip() == '':
            raise Exception('Tablename cannot be None or empty')

        if kwargs.get('Key') is None:
            raise Exception('Key cannot be None')
        elif not isinstance(kwargs.get('Key'), dict):
            raise Exception('Key must be a dict object')
        elif len(kwargs.get('Key')) < 1:
            raise Exception('Key must not be empty')

        if kwargs.get('Key').get('id').get('S') == 'testing-get-pet':
            return {
                'Item':
                {
                    'gender': {'S': 'female'},
                    'species': {'S': 'cat'},
                    'name': {'S': 'fluffy'},
                    'id': {'S': 'testing-get-pet'},
                    'age': {'N': '0'},
                    'breed': {'S': 'angora'},
                    'zip_code': {'S': '90210'}
                    }
            }
        else:
            return {}

    def scan(self, **kwargs):
        if kwargs.get('TableName') is None or \
         kwargs.get('TableName').strip() == '':
            raise Exception('Tablename cannot be None or empty')

        return {
            'Items': [
                        {
                          'gender': {'S': 'female'},
                          'species': {'S': 'cat'},
                          'name': {'S': 'fluffy'},
                          'id': {'S': 'testing-get-pet-1'},
                          'age': {'N': '0'},
                          'breed': {'S': 'angora'},
                          'zip_code': {'S': '90210'}
                        },
                        {
                          'gender': {'S': 'female'},
                          'species': {'S': 'cat'},
                          'name': {'S': 'fluffy'},
                          'id': {'S': 'testing-get-pet-2'},
                          'age': {'N': '0'},
                          'breed': {'S': 'angora'},
                          'zip_code': {'S': '90210'}
                        },
                        {
                          'gender': {'S': 'female'},
                          'species': {'S': 'cat'},
                          'name': {'S': 'fluffy'},
                          'id': {'S': 'testing-get-pet-3'},
                          'age': {'N': '0'},
                          'breed': {'S': 'angora'},
                          'zip_code': {'S': '90210'}
                        }
                ]
        }

    def put_item(self, **kwargs):
        if kwargs.get('TableName') is None or \
         kwargs.get('TableName').strip() == '':
            raise Exception('Tablename cannot be None or empty')

        if kwargs.get('Item') is None:
            raise Exception('Item cannot be None')
        elif not isinstance(kwargs.get('Item'), dict):
            raise Exception('Item must be a dict object')
        elif len(kwargs.get('Item')) < 1:
            raise Exception('Item must not be empty')

        return True


class PetServiceTest(unittest.TestCase):
    def setUp(self):
        client = MockClient()
        self.config = {'PETS_TABLE': 'pets'}
        self.service = PetService(client=client, config=self.config)

    def test_get_pet(self):
        pet = self.service.get_pet(pet_id='testing-get-pet')
        self.assertTrue(isinstance(pet, Pet))

    def test_get_pet_does_not_exist(self):
        with self.assertRaises(DoesNotExist):
            self.service.get_pet(pet_id='testing-get-pet-not-exist')

    def test_get_pets(self):
        pets = self.service.get_pets()
        for pet in pets:
            self.assertTrue(isinstance(pet, Pet))

    def test_get_pets_no_pets(self):
        class SubMockClient(MockClient):
            def __init__(self):
                pass

            def scan(self, **kwargs):
                super().scan(**kwargs)
                return {'Items': []}

        service = PetService(client=SubMockClient(), config=self.config)

        pets = list(service.get_pets())
        self.assertTrue(len(pets) == 0)

    def test_insert_pet(self):
        pet = {
            'age': 0,
            'breed': 'angora',
            'gender': 'female',
            'id': '9469d54a-aef2-11e9-9ceb-3af9d32ee3fa',
            'name': 'fluffy',
            'species': 'cat',
            'zip_code': '90210'
        }

        pet = self.service.insert_pet(**pet)
        self.assertTrue(isinstance(pet, Pet))
        self.assertTrue(pet.id != '9469d54a-aef2-11e9-9ceb-3af9d32ee3fa')

    def tearDown(self):
        self.service = None
