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

    def test_add_pdf_attachment(self):
        try:
            with open("attachment.pdf", 'rb') as f:
                attachment_binary = f.read()
            attachment_integer = int.from_bytes(attachment_binary, byteorder='big')
            data = {
                'attachment_integer': attachment_integer,
                'name_of_attachment': "pdf_attachment"
            }
            rv = self.app.post('/add_attachment', data=json.dumps(data), content_type='application/json')
        except IOError:
            print("File is not there")

    def test_get_pdf_attachment(self):

        rv = self.app.get('/add_attachment', data=json.dumps([]), content_type='application/json')

        assert b'got the picture' in rv.data


if __name__ == '__main__':
    unittest.main()
