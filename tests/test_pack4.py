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

    def _test_add_question(self):

        test = Test('tester@tester.com')
        test.insert_test('What is 1 + 1?', '3', '4', '5', '2')


    def test_retrieve_questions(self):
        test = Test('tester@tester.com')
        data = test.get_num_records()
        # print("Number of records: " + str(data))
        data = test.get_tests()
        # print(data)






if __name__ == '__main__':
    unittest.main()
