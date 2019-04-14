import unittest
from faker import Faker
import app
import json
import psycopg2


class AddPhoto(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def add_test_photo(self):

        photo_extension = "png"
        photo_binary = open("tests/test_image.jpg", 'rb').read()
        photo_binary = psycopg2.Binary(photo_binary)
        data = {
            'username': 'tester@tester.com',
            'photo_extension': photo_extension,
            'photo_binay': photo_binary
        }
        rv = self.app.post('/add_photo', data=json.dumps(data), content_type='application/json')
        assert b'added photo successfully' in rv.data


if __name__ == '__main__':

    unittest.main()
