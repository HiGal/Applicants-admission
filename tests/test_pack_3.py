import base64
import unittest
import app
import json
import os


class AddPhoto(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_add_test_photo(self):
        try:
            path = os.path.dirname(os.path.realpath(__file__)) + "/test_image.jpg"
            with open(path, 'rb') as f:
                photo_extension = "png"
                photo_binary = f.read()
                print(photo_binary)

            zinj = photo_binary.decode()
            bin = zinj.encode()
            if bin == photo_binary:
                print("Hurray")
            # photo_binary = str(photo_binary, 'utf-8', 'ignore')

            return
            data = {
                'username': 'tester@tester.com',
                'photo_extension': 'jpg',
                'photo_binary': photo_binary
            }

            rv = self.app.post('/add_profile_picture', data=json.dumps(data), content_type='application/json')
            # print(rv.data)
            assert b'added photo successfully' in rv.data

        except IOError:
            print("file does not exist")


if __name__ == '__main__':
    unittest.main()
