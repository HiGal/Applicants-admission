import unittest
from faker import Faker
import app
import json
import random


class PersonalInfoTest(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def generate_data(self): # username, fname, sname, bdate, gender, citizenship
        faker = Faker()
        profile = faker.simple_profile()
        name, sname = profile['name'].split()[0], profile['name'].split()[1]
        birthdate = profile['birthdate'].strftime("%Y-%m-%d")
        country = faker.country()

        data_pack = {
            'username': name+sname,
            'fname': name,
            'sname': sname,
            'bdate': birthdate,
            'citizenship': country,
            'gender': random.choice(['M', 'F', 'Dont want to specify'])
        }
        return data_pack

    # Test when password and check password field are the same


    def test_update_info(self):
        data = self.generate_data()
        rv = self.app.post('/personal-info', data=json.dumps(data), content_type='application/json')
        assert b'Basic info successfully created' in rv.data


if __name__ == '__main__':
    unittest.main()
