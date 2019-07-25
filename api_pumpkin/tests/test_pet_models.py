from api_pumpkin.models.pet import Pet, PetCat, PetDog
import unittest


class PetModelsTest(unittest.TestCase):
    def test_properties(self):
        pet_dict = {
            'id': 1,
            'age': 2,
            'breed': 'golden_retriever',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }
        pet = Pet(**pet_dict)
        self.assertEqual(pet.id, 1)
        self.assertEqual(pet.age, 2)
        self.assertEqual(pet.breed, 'golden_retriever')
        self.assertEqual(pet.zip_code, '10704')
        self.assertEqual(pet.gender, 'male')
        self.assertEqual(pet.name, 'Spot')
        self.assertEqual(pet.species, 'dog')

    def test_age_validation(self):
        pet_dict = {
            'age': '2',
            'breed': 'golden_retriever',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

    def test_breed_validation(self):
        pet_dict = {
            'age': 2,
            'breed': 1,
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

        pet_dict['breed'] = ''

        with self.assertRaises(ValueError):
            pet = Pet(**pet_dict)

    def test_zip_code_validation(self):
        pet_dict = {
            'age': 2,
            'breed': 'golden_retriever',
            'zip_code': 10704,
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

        pet_dict['zip_code'] = '1070'
        with self.assertRaises(ValueError):
            pet = Pet(**pet_dict)

        pet_dict['zip_code'] = '10702334'
        with self.assertRaises(ValueError):
            pet = Pet(**pet_dict)

    def test_gender_validation(self):
        pet_dict = {
            'age': 2,
            'breed': 'golden_retriever',
            'zip_code': '10704',
            'gender': 1,
            'name': 'Spot',
            'species': 'dog'
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

        pet_dict['gender'] = 'not_male'
        with self.assertRaises(ValueError):
            pet = Pet(**pet_dict)

    def test_species_validation(self):
        pet_dict = {
            'age': 2,
            'breed': 'golden_retriever',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Spot',
            'species': 1
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

        pet_dict['species'] = 'whale'
        with self.assertRaises(ValueError):
            pet = Pet(**pet_dict)

    def test_name_validation(self):
        pet_dict = {
            'age': 2,
            'breed': 'golden_retriever',
            'zip_code': '10704',
            'gender': 'male',
            'name': 1,
            'species': 'dog'
        }

        with self.assertRaises(TypeError):
            pet = Pet(**pet_dict)

    def test_quote_base(self):
        pet_dict = {
            'id': 1,
            'age': 2,
            'breed': 'maine_coon',
            'zip_code': '90210',
            'gender': 'male',
            'name': 'George',
            'species': 'cat'
        }
        pet = Pet(**pet_dict)
        self.assertEqual(pet.quote(), 135.8550)

    def test_quote_cat(self):
        cat_dict = {
            'id': 1,
            'age': 2,
            'breed': 'siamese',
            'zip_code': '90210',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'cat'
        }
        cat = PetCat(**cat_dict)
        self.assertEqual(cat.quote(), 181.3050)

    def test_quote_dog(self):
        dog_dict = {
            'id': 1,
            'age': 3,
            'breed': 'golden_retriever',
            'zip_code': '02481',
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }
        dog = PetDog(**dog_dict)
        self.assertEqual(dog.quote(), 182.3850)

    def test_quote_cat_default_breed(self):
        cat_dict = {
            'id': 1,
            'age': 2,
            'breed': 'angora',
            'zip_code': '02481',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'cat'
        }
        cat = PetCat(**cat_dict)
        self.assertEqual(cat.quote(), 181.4850)

    def test_quote_dog_default_breed(self):
        dog_dict = {
            'id': 1,
            'age': 3,
            'breed': 'bull_dog',
            'zip_code': '02481',
            'gender': 'male',
            'name': 'Spot',
            'species': 'dog'
        }
        dog = PetDog(**dog_dict)
        self.assertEqual(dog.quote(), 182.1600)

    def test_quote_default_zip_code(self):
        cat_dict = {
            'id': 1,
            'age': 2,
            'breed': 'siamese',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'cat'
        }
        cat = PetCat(**cat_dict)
        self.assertEqual(cat.quote(), 181.4400)

    def test_quote_age_less_than_one(self):
        cat_dict = {
            'id': 1,
            'age': 0,
            'breed': 'siamese',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'cat'
        }
        cat = PetCat(**cat_dict)
        self.assertEqual(cat.quote(), 181.0350)

    def test_quote_age_greater_than_eight(self):
        cat_dict = {
            'id': 1,
            'age': 9,
            'breed': 'siamese',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'cat'
        }
        cat = PetCat(**cat_dict)
        self.assertEqual(cat.quote(), 183.0600)

    def test_unsupported_species(self):
        bird_dict = {
            'id': 1,
            'age': 9,
            'breed': 'siamese',
            'zip_code': '10704',
            'gender': 'male',
            'name': 'Fluffy',
            'species': 'bird'
        }

        with self.assertRaises(ValueError):
            bird = Pet(**bird_dict)
