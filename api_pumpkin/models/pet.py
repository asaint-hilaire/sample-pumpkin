import uuid
import re


class Pet(object):
    BASE_PRICE = 45

    def __init__(self, **kwargs):
        self._set_id(kwargs.get('id'))
        self._set_age(kwargs.get('age'))
        self._set_breed(kwargs.get('breed'))
        self._set_zip_code(kwargs.get('zip_code'))
        self._set_gender(kwargs.get('gender'))
        self._set_name(kwargs.get('name'))
        self._set_species(kwargs.get('species'))

    def _get_id(self):
        return self._id

    def _set_id(self, id):
        if id is None:
            self._id = str(uuid.uuid1())
        else:
            self._id = id

    def _get_age(self):
        return self._age

    def _set_age(self, age):
        if isinstance(age, int):
            self._age = age
        else:
            raise TypeError('Age must be an integer type')

    def _get_breed(self):
        return self._breed

    def _set_breed(self, breed):
        if isinstance(breed, str):
            if breed.strip() == '':
                raise ValueError('Breed cannot be empty')
            self._breed = breed.lower()
        else:
            raise TypeError('Breed must be a string')

    def _get_zip_code(self):
        return self._zip_code

    def _set_zip_code(self, zip_code):
        if isinstance(zip_code, str):
            if re.match(r'\d{5}$', zip_code):
                self._zip_code = zip_code
            else:
                raise ValueError('Zip code must be 5 digits long e.g. 00000')
        else:
            raise TypeError('Zip code must be a string')

    def _get_gender(self):
        return self._gender

    def _set_gender(self, gender):
        supported = ['female', 'male']
        if isinstance(gender, str):
            gender = gender.lower()
            if gender in supported:
                self._gender = gender
            else:
                raise ValueError(f'Supported genders {supported}')
        else:
            raise TypeError('Gender must be a string')

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError('Name must be a string')

    def _get_species(self):
        return self._species

    def _set_species(self, species):
        supported = ['cat', 'dog']
        if isinstance(species, str):
            species = species.lower()
            if species in supported:
                self._species = species
            else:
                raise ValueError(f'Supported species {supported}')
        else:
            raise TypeError('Species must be a string')

    id = property(_get_id, _set_id)
    age = property(_get_age, _set_age)
    breed = property(_get_breed, _set_breed)
    zip_code = property(_get_zip_code, _set_zip_code)
    gender = property(_get_gender, _set_gender)
    name = property(_get_name, _set_name)
    species = property(_get_species, _set_species)

    def quote(self):
        age_factors = {'<1': 1.01, '1': 1.015, '2': 1.019, '3': 1.024,
                       '4': 1.028, '5': 1.03, '6': 1.034, '7': 1.038,
                       '8': 1.044, '>8': 1.055}
        zipcode_factors = {'90210': 1.01, '10001': 1.015, '02481': 1.019,
                           '11217': 1.024, 'DEFAULT': 1.013}
        species_factors = {'dog': 1, 'cat': 0.99}

        sum = 0
        if self.age < 1:
            sum += age_factors.get('<1')
        elif self.age > 8:
            sum += age_factors.get('>8')
        else:
            sum += age_factors.get(str(self.age))

        if zipcode_factors.get(self.zip_code) is not None:
            sum += zipcode_factors.get(self.zip_code)
        else:
            sum += zipcode_factors.get('DEFAULT')

        if species_factors.get(self.species) is not None:
            sum += species_factors.get(self.species)
        else:
            raise Exception(
                f'No calculation implemented for {self._species} species')

        return round(self.BASE_PRICE * (sum), 4)

    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age,
            'breed': self.breed,
            'zip_code': self.zip_code,
            'gender': self.gender,
            'name': self.name,
            'species': self.species,
        }


class PetDog(Pet):
    def __init__(self, **kwargs):
        kwargs['species'] = 'dog'
        super().__init__(**kwargs)

    species = property(Pet._get_species)

    def quote(self):
        dog_breed_factors = {'golden_retriever': 1.01, 'dachshund': 1.015,
                             'chesapeake_bay_retriever': 1.002,
                             'DEFAULT': 1.005}

        return round(
            (super().quote() + self.BASE_PRICE *
                (dog_breed_factors.get(self.breed)
                 if dog_breed_factors.get(self.breed) is not None
                 else dog_breed_factors.get('DEFAULT'))),  4)


class PetCat(Pet):
    def __init__(self, **kwargs):
        kwargs['species'] = 'cat'
        super().__init__(**kwargs)

    species = property(Pet._get_species)

    def quote(self):
        cat_breed_factors = {'siamese': 1.01, 'maine_coon': 1.015,
                             'ragdoll': 1.002, 'DEFAULT': 1.005}

        return round(
            (super().quote() + self.BASE_PRICE *
                (cat_breed_factors.get(self.breed)
                 if cat_breed_factors.get(self.breed) is not None
                 else cat_breed_factors.get('DEFAULT'))), 4)


def PetFactory(**kwargs):
    if isinstance(kwargs.get('species'), str):
        if kwargs.get('species').lower() == 'dog':
            return PetDog(**kwargs)
        elif kwargs.get('species').lower() == 'cat':
            return PetCat(**kwargs)
    return Pet(**kwargs)
