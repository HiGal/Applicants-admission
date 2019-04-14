import base64
import unittest

import app
import json
import os


class AddPhoto(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    '''print(photo_binary)
            encoded = base64.encodebytes(photo_binary)
            print(encoded)
            print("\n")
            zinj = encoded.decode('ascii')
            # print(zinj)'''

    def test_add_test_photo(self):
        try:
            path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.jpg"
            with open(path, 'rb') as f:
                photo_extension = "jpg"
                photo_binary = f.read()
                f.close()
            # print(photo_binary)
            photo_integer = int.from_bytes(photo_binary, byteorder='big')

            data = {
                'username': 'tester@tester.com',
                'photo_extension': 'jpg',
                'photo_binary': photo_integer,
                'byte_count': len(photo_binary)
            }

            rv = self.app.post('/profile_picture', data=json.dumps(data), content_type='application/json')
            assert b'added photo successfully' in rv.data

        except IOError:
            print("file does not exist")

    def test_get_profile_picture(self):
        rv = self.app.get('/profile_picture', data=json.dumps([]), content_type='application/json')

        assert b'got the picture' in rv.data


if __name__ == '__main__':
    unittest.main()
