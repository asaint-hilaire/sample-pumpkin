from api_pumpkin.models.pet import PetFactory
from api_pumpkin.utils.exceptions import DoesNotExist


class PetService(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def get_pet(self, pet_id):
        resp = self.client.get_item(
            TableName=self.config.get('PETS_TABLE'),
            Key={
                'id': {'S': pet_id}
            }
        )

        item = resp.get('Item')
        if not item:
            raise DoesNotExist()

        return PetFactory(
                id=item.get('id').get('S'),
                name=item.get('name').get('S'),
                age=int(item.get('age').get('N')),
                breed=item.get('breed').get('S'),
                gender=item.get('gender').get('S'),
                species=item.get('species').get('S'),
                zip_code=item.get('zip_code').get('S'),
            )

    def get_pets(self):
        resp = self.client.scan(TableName=self.config.get('PETS_TABLE'))
        for item in resp.get('Items'):
            yield PetFactory(
                id=item.get('id').get('S'),
                name=item.get('name').get('S'),
                age=int(item.get('age').get('N')),
                breed=item.get('breed').get('S'),
                gender=item.get('gender').get('S'),
                species=item.get('species').get('S'),
                zip_code=item.get('zip_code').get('S'),
            )

    def insert_pet(self, **kwargs):
        if kwargs.get('id') is not None:
            del kwargs['id']

        pet = PetFactory(**kwargs)
        resp = self.client.put_item(
            TableName=self.config.get('PETS_TABLE'),
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

        return pet
