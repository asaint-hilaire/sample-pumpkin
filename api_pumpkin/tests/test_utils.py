from api_pumpkin.utils.exceptions import DoesNotExist
from api_pumpkin.utils.helper import response
import unittest


class UtilsTest(unittest.TestCase):
    def test_exception_does_not_exist(self):
        try:
            raise DoesNotExist
        except DoesNotExist as ex:
            self.assertTrue('Object does not exist' == str(ex))

    def test_helper_response(self):
        resp = response(error='error', payload={'data': 'data'})
        self.assertTrue(resp.get('error') == 'error')
        self.assertTrue(resp.get('body').get('data') == 'data')


if __name__ == '__main__':
    unittest.main()
