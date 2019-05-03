import unittest
from faker import Faker
import app
import json


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def generate_data(self):
        faker = Faker()
        profile = faker.simple_profile()
        name, sname = profile['name'].split()[0], profile['name'].split()[1]
        email = profile['mail']
        birthdate = profile['birthdate'].strftime("%Y-%m-%d")
        password = profile['username']
        data_pack = {
            'name': name,
            'sname': sname,
            'email': email,
            'bdate': birthdate,
            'password': password,
            'cpassword': password
        }
        return data_pack

    # Test when password and check password field are the same
    def test_registration_1(self):
        data = self.generate_data()
        rv = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        assert b'Account successfully created' in rv.data

    # Test when password and check password field are not the same
    def test_registration_2(self):
        data = self.generate_data()
        data['cpassword'] = data['cpassword'] + 'ad'
        rv = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        assert b'Password are not the same!' in rv.data

    def test_login(self):
        data_corr = {
            'username': 'tester@tester.com',
            'password': '123123'
        }
        rv = self.app.post('/login', data=json.dumps(data_corr), content_type='application/json')
        # print(rv.data)
        print(rv.data)
        assert b'Username or Password incorrect' == rv.data

        data_incorr1 = {
            'username': 'f.galeev',
            'password': '123'
        }
        rv = self.app.post('/login', data=json.dumps(data_incorr1), content_type='application/json')
        assert b'Username or Password incorrect' == rv.data

        data_incorr2 = {
            'username': 'f.galeev@innopolis.ru',
            'password': '1234'
        }
        rv = self.app.post('/login', data=json.dumps(data_incorr2), content_type='application/json')
        print(rv)
        print("this ^")
        assert b'Username or Password incorrect' == rv.data


if __name__ == '__main__':
    unittest.main()
