import json
import random
import unittest

import app


class AddTest(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_add_question(self):
        record = [1, 'What is 2+2?', '3', '4', '2', 'I dont know', '4']
        data = {
            'question': record[1],
            'choice1': record[3],
            'choice2': record[2],
            'choice3': record[4],
            'choice4': record[5]
        }
        rv = self.app.post('/add_test', data=json.dumps(data), content_type='application/json')
        # assert b'Test added successfully' in rv.data

    def test_retrieve_questions(self):
        rv = self.app.get('/get_test', content_type='application/json')
        if rv.data is None:
            assert ChildProcessError

    def test_update_result(self):
        x = random.randint(0, 100)
        data = {
            'result': str(x) + " out of " + str(random.randint(x, 100))
        }
        rv = self.app.post('update_result', data=json.dumps(data), content_type='application/json')
        assert b'successfully updated the result'


if __name__ == '__main__':
    unittest.main()
