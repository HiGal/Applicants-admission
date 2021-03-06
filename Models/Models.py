import base64
import os

import psycopg2

from Security import SecretConstants, Secure


def db_connect():
    dbname = SecretConstants.DATABASE_NAME
    user = SecretConstants.DATABASE_USER
    password = SecretConstants.DATABASE_PASSWORD
    host = SecretConstants.DATABASE_HOST

    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)


class User:
    def __init__(self, username=None, password=None):
        self.conn = db_connect()
        self.username = username
        self.password = password
        self.type = 'student'

    def get_type(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT is_professor FROM sys_user WHERE username = %s;',
            [self.username]
        )
        if cursor.rowcount == 0:
            return 'student'
        record = next(cursor)
        if record[0]:
            self.type = 'professor'
        else:
            self.type = 'student'
        return self.type

    def verify(self):
        cursor = self.conn.cursor()
        password = self.password
        cursor.execute(
            'SELECT * FROM sys_user WHERE username = %s AND password = %s;',
            (self.username, password)
        )

        if cursor.rowcount != 0:
            cursor.close()
            return True

        cursor.close()
        return False

    def register(self, username, password, name, sname, email, bdate):
        self.password = password
        self.username = username
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO sys_user (username, password, name, surname, email, birthday) '
            'VALUES (%s, %s, %s, %s, %s, %s);',
            (username, password, name, sname, email, bdate)
        )
        self.conn.commit()
        cursor.close()

    def contacts(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_contact WHERE uname = %s;', [self.username])

        if cursor.rowcount == 0:
            cursor.close()
            return None

        record = next(cursor)
        data = {
            'index': record[0],
            'region': record[1],
            'city': record[2],
            'street': record[3],
            'building': record[4],
            'corpus': record[5],
            'flat': record[6]
        }

        cursor.close()

        return data

    def update_contacts(self, index, region, city, street, building, corpus, flat):
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM user_contact WHERE uname = %s;', [self.username])

        if cursor.rowcount != 0:
            cursor.execute(
                'UPDATE user_contact '
                'SET index = %s, region = %s, city = %s, street = %s, building = %s, corpus = %s, flat = %s '
                'WHERE uname = %s;',
                (index, region, city, street, building, corpus, flat, self.username)
            )
        else:
            cursor.execute(
                'INSERT INTO user_contact (index, region, city, street, building, corpus, flat, uname) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
                (index, region, city, street, building, corpus, flat, self.username)
            )

        self.conn.commit()
        cursor.close()

    def get_info(self):
        cursor = self.conn.cursor()
        # MAKE SURE THAT YOU DISABLED TESTING !
        cursor.execute('SELECT * FROM sys_user WHERE username = %s;', [self.username])
        print(self.username)
        record = next(cursor)
        cursor.close()

        data = {
            'name': record[2],
            'surname': record[3],
            'email': record[4],
            'birthday': record[5],
            'gender': record[6],
            'citizen': record[7],
            'photo_data': self.get_photo(self.username)
        }

        return data

    def update_info(self, fname, sname, bdate, gender, citizenship):

        stuff = self.get_info()
        # print(stuff)
        if not bdate:
            bdate = stuff['birthday']
        if not gender:
            gender = stuff['gender']
        cursor = self.conn.cursor()

        cursor.execute(
            'UPDATE sys_user SET name = %s, surname = %s, birthday = %s, sex = %s, citizen = %s '
            'WHERE username = %s;',
            (fname, sname, bdate, gender, citizenship, self.username)
        )
        self.conn.commit()
        cursor.close()

    def add_photo(self, photo_binary_data, username):
        # this function is to insert photos in the database
        # Decode as integer and send to server and then decode it to binary form
        query = """update sys_user set photo_data = '%s' where username= '%s'""" % (photo_binary_data, username)
        cursor = self.conn.cursor()
        # print(query)
        cursor.execute(query)
        self.conn.commit()

        cursor.close()

    def get_photo(self, username):
        try:
            query = """select photo_data from sys_user where username = '%s';""" % username

            path = os.path.dirname(os.path.realpath(__file__))
            print(path)
            # print(query)

            cursor = self.conn.cursor()
            cursor.execute(query)
            photo_data = cursor.fetchall()[0][0]
            print(path + "/../static/img/profile.png")
            if photo_data is None:
                with open(path + "/../static/img/profile.png", "rb") as f:
                    photo_data = f.read()
                photo_data = base64.b64encode(photo_data).decode('ascii')

            cursor.close()
            return photo_data

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


class PassportData:
    from typing import Optional

    def __init__(self, username, passport_series=None, passport_number=None, issue_date=None,
                 issuing_authority=None):
        self.conn = db_connect()
        self.username = username
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.issue_date = issue_date
        self.issuing_authority = issuing_authority

    def __get_user_hashed_pass__(self, cursor) -> Optional[str]:
        cursor.execute(
            'SELECT password FROM sys_user '
            'WHERE username = %s;', [self.username]
        )

        if cursor.rowcount == 0:
            cursor.close()
            return None

        record = next(cursor)

        return record[0]

    def register(self, passport_series: str, passport_num: str, issue_date: str, issuing_authority: str):
        cursor = self.conn.cursor()

        user_password = self.__get_user_hashed_pass__(cursor)
        if not user_password:
            return False

        encryption_key = Secure.create_key(user_password.encode(), SecretConstants.PASSPORT_ENCRYPTION_SALT)

        series = Secure.encrypt(passport_series.encode(), encryption_key).decode()
        number = Secure.encrypt(passport_num.encode(), encryption_key).decode()
        date = Secure.encrypt(issue_date.encode(), encryption_key).decode()
        authority = Secure.encrypt(issuing_authority.encode(), encryption_key).decode()

        cursor.execute('SELECT username FROM passport_data WHERE passport_data.username = %s;', [self.username])
        if cursor.rowcount != 0:
            cursor.execute(
                'UPDATE passport_data '
                'SET passport_series = %s, passport_number = %s, issue_date = %s, issuing_authority = %s '
                'WHERE username = %s;',
                (series, number, date, authority, self.username)
            )
        else:
            cursor.execute(
                'INSERT INTO passport_data '
                '(username, passport_series, passport_number, issue_date, issuing_authority) '
                'VALUES (%s, %s, %s, %s, %s);',
                (self.username, series, number, date, authority)
            )

        self.conn.commit()
        cursor.close()

    def retrieve(self) -> bool:
        cursor = self.conn.cursor()

        user_password = self.__get_user_hashed_pass__(cursor)
        if not user_password:
            return False

        cursor.execute(
            'SELECT * FROM passport_data '
            'WHERE username = %s;', [self.username]
        )

        if cursor.rowcount == 0:
            cursor.close()
            return False

        record = next(cursor)
        cursor.close()

        encryption_key = Secure.create_key(user_password.encode(), SecretConstants.PASSPORT_ENCRYPTION_SALT)

        self.passport_series = Secure.decrypt(record[1].encode(), encryption_key).decode()
        self.passport_number = Secure.decrypt(record[2].encode(), encryption_key).decode()
        self.issue_date = Secure.decrypt(record[3].encode(), encryption_key).decode()
        self.issuing_authority = Secure.decrypt(record[4].encode(), encryption_key).decode()

        return True

    def get_data_without_db(self):
        return {'passport_series': self.passport_series, 'passport_number': self.passport_number,
                'issue_date': self.issue_date, 'issuing_authority': self.issuing_authority}


class Portfolio:
    def __init__(self, username: str):
        self.conn = db_connect()
        self.username = username
        self.document = b'0'
        self.byte_count = 0

    def insert_file(self, document):

        cursor = self.conn.cursor()
        print(self.username)
        print(document)

        cursor.execute(
            'SELECT username FROM portfolios WHERE username = %s;',
            [self.username]
        )

        if cursor.rowcount == 0:
            cursor.execute(
                'INSERT INTO portfolios (username, document) '
                'VALUES (%s, %s)', (self.username, document)
            )
        else:
            cursor.execute(
                'UPDATE portfolios '
                'SET document = %s '
                'WHERE username = %s;',
                (document, self.username)
            )

        self.conn.commit()
        cursor.close()

        self.document = document

        print("returned")
        return True

    def insert_result(self, result):
        cursor = self.conn.cursor()
        print(self.username)

        cursor.execute(
            'SELECT username FROM portfolios WHERE username = %s;',
            [self.username]
        )

        if cursor.rowcount == 0:
            cursor.execute(
                'INSERT INTO portfolios (username, test_result) '
                'VALUES (%s, %s)', (self.username, result)
            )
        else:
            cursor.execute(
                'UPDATE portfolios '
                'SET test_result = %s '
                'WHERE username = %s;',
                (result, self.username)
            )

        self.conn.commit()
        cursor.close()

        return True

    def get_test_and_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM Portfolios;'
        )
        arr = []
        for record in cursor:
            data = {
                'email': record[0],
                'test_result': record[2]
            }
            arr.append(data)
        frr = []
        for data in arr:
            cursor.execute(
                'select name, surname, citizen from sys_user where username = %s',
                [data['email']]
            )
            if cursor.rowcount == 0:
                continue
            if data['test_result'] is None:
                data['test_result'] = 'Not Yet Performed'
            record = next(cursor)
            rdata = {
                'email': data['email'],
                'test_result': data['test_result'],
                'name': record[0],
                'surname': record[1],
                'citizen': record[2]
            }
            if rdata['citizen'] is None:
                rdata['citizen'] = 'User hasnt chosen yet'
            frr.append(rdata)
        return frr

    def retrieve(self):
        cursor = self.conn.cursor()
        print(self.username)
        cursor.execute(
            'SELECT document FROM portfolios '
            'WHERE username = %s;',
            [self.username]
        )

        if cursor.rowcount == 0:
            return 0

        record = next(cursor)
        cursor.close()
        return {'attachment': record[0]}


class Test:
    def __init__(self, username):
        self.conn = db_connect()
        self.username = username

    def get_tests(self):
        cursor = self.conn.cursor()

        cursor.execute(
            'SELECT * FROM tests_questions;'
        )
        if cursor.rowcount == 0:
            cursor.close()
            assert AssertionError

        array_of_records = []
        # print(records)
        for record in cursor:
            ans_letters = '__abcd'
            answer = 'a'
            for i in [2, 3, 4, 5]:
                if record[i] == record[6]:
                    answer = ans_letters[i]
                    break
            data = {
                'question': record[1],
                'answers': {
                    'a': record[2],
                    'b': record[3],
                    'c': record[4],
                    'd': record[5]
                },
                'correctAnswer': answer
            }
            array_of_records.append(data)

        return array_of_records

    def get_num_records(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM tests_questions;'
        )
        ret = next(cursor)[0]
        cursor.close()
        return ret

    def insert_test(self, question: str, choice1: str, choice2: str, choice3: str, choice4: str, correct_choice: str):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO tests_questions (question, choice1, choice2, choice3, choice4, correct_choice) '
            'VALUES (%s, %s, %s, %s, %s, %s);',
            (question, choice1, choice2, choice3, choice4, correct_choice)
        )
        self.conn.commit()
        cursor.close()

