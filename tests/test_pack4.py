import base64
import unittest

import app
import json
import os


# from Models.Models import *


class AddTest(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_add_question(self):
        record = [1, 'What is 2+2?', '3', '4', '2', 'I dont know','5']
        data = {
            'question': record[1],
            'choice1': record[2],
            'choice2': record[3],
            'choice3': record[4],
            'choice4': record[5],
            'correct_choice': record[6]
        }
        rv = self.app.post('/add_test', data=json.dumps(data), content_type='application/json')
        assert b'Test added successfully' in rv.data

    def test_retrieve_questions(self):
        rv = self.app.get('/get_test', content_type='application/json')
        # print(rv.data)
        assert b'data fetched correctly' in rv.data


if __name__ == '__main__':
    unittest.main()
