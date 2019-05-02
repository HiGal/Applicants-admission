import base64
import os
from typing import Dict, Optional

import psycopg2

from Security import SecretConstants, Secure


def db_connect():
    dbname = SecretConstants.DATABASE_NAME
    user = SecretConstants.DATABASE_USER
    password = SecretConstants.DATABASE_PASSWORD
    host = SecretConstants.DATABASE_HOST

    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)


class User:
    """
    Model defines the User.
    """

    def __init__(self, username: str = None, password: str = None):
        """
        Create the new User.

        Arguments are not needed for registration.

        :param username: Username
        :param password: Password
        """
        self.conn = db_connect()
        self.username = username
        self.password = password

    def verify(self) -> bool:
        """
        Authorize the user.

        Credentials should be set before verifying.

        :return: True if successfully authorized, False otherwise
        """
        cursor = self.conn.cursor()
        password = self.password
        password = Secure.hash_password(password)
        cursor.execute(
            'SELECT * FROM sys_user WHERE username = %s AND password = %s;',
            (self.username, password)
        )

        if cursor.rowcount != 0:
            cursor.close()
            return True

        cursor.close()
        return False

    def register(self, username: str, password: str, name: str, sname: str, email: str, bdate: str):
        """
        Register the new user.

        :param username: Username
        :param password: Password
        :param name: Name (first name)
        :param sname: Surname (last name)
        :param email: Email
        :param bdate: Birth date in format yyyy-mm-dd
        """
        password = Secure.hash_password(password)
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

    def contacts(self) -> Optional[Dict[str, str, str, str, str, str, str]]:
        """
        Retrieve the user contacts.

        :return: Dictionary in format `{ index: str, region: str,
        city: str, street: str, building: str, corpus: str, flat: str }`
        """
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

    def update_contacts(self, index: str, region: str, city: str, street: str, building: str, corpus: str, flat: str):
        """
        Update user contacts.

        :param index: Index
        :param region: Region
        :param city: City
        :param street: Street
        :param building: Building
        :param corpus: Corpus
        :param flat: Flat
        """
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

    def get_info(self) -> Dict[str, str, str, str, str, str]:
        """
        Get main user information.

        MAKE SURE YOU HAVE TURNED OFF THE TESTING FLAG!

        :return: Dictionary in in format `{ name: str, surname: str, email: str, birthday: str, gender: str, citizen: str }`
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM sys_user WHERE username = %s;', [self.username])
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

    def update_info(self, fname: str, sname: str, bdate: str, gender: str, citizenship: str):
        """
        Update main user info.

        :param fname: First name
        :param sname: Surname (last name)
        :param bdate: Birth date in format `yyyy-mm-dd`
        :param gender: Gender (M / F / ND)
        :param citizenship: Citizenship country
        """
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

    def add_photo(self, photo_extension: str, photo_binary_data: int, byte_count: int, username: str):
        """
        Insert user profile photo into database.

        Decode as integer and send to server and then decode it to binary form.

        :param photo_extension: Photo file extension
        :param photo_binary_data: Photo data
        :param byte_count: Number of bytes in photo data
        :param username: User username
        """

        photo_binary_data = photo_binary_data.to_bytes(byte_count, byteorder='big')

        photo_binary_data = psycopg2.Binary(photo_binary_data)

        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE user_contact '
            'SET photo_extension = %s, photo_data = %s '
            'WHERE uname = %s;',
            (photo_extension, photo_binary_data, username)
        )

        self.conn.commit()

        cursor.close()

    def get_photo(self, username: str) -> Optional[Dict[str, int]]:
        """
        Retrieve the user profile photo from database.

        :param username: Username
        :return: Dictionary in format `{ photo_integer, byte_count }`
        """
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT photo_data FROM sys_user '
                'WHERE username = %s;', [username]
            )
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
    """
    Model defines the passport data.
    """
    from typing import Optional

    def __init__(self, username, passport_series=None, passport_number=None, issue_date=None,
                 issuing_authority=None):
        """
        Create new Passport Data object.

        :param username: Corresponding username
        :param passport_series: Passport series
        :param passport_number: Passport number
        :param issue_date: Document issue date
        :param issuing_authority: Document issuing authority
        """
        self.conn = db_connect()
        self.username = username
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.issue_date = issue_date
        self.issuing_authority = issuing_authority

    def __get_user_hashed_pass__(self, cursor) -> Optional[str]:
        """
        (KINDA PRIVATE) User hashed pass.

        :param cursor: Database cursor
        :return: User hashed pass
        """
        cursor.execute(
            'SELECT password FROM sys_user '
            'WHERE username = %s;', [self.username]
        )

        if cursor.rowcount == 0:
            cursor.close()
            return None

        record = next(cursor)

        return record[0]

    def register(self, passport_series: str, passport_num: str, issue_date: str, issuing_authority: str) -> bool:
        """
        Register new passport data.

        Uses the user password to encrypt the data.

        :param passport_series: Passport series
        :param passport_num: Passport number
        :param issue_date: Document issue date
        :param issuing_authority: Document issuing authority
        :return: False if user not found, True on success
        """
        cursor = self.conn.cursor()

        user_password = self.__get_user_hashed_pass__(cursor)
        if not user_password:
            return False

        encryption_key = Secure.create_key(user_password.encode(), SecretConstants.PASSPORT_ENCRYPTION_SALT)

        series = Secure.encrypt(passport_series.encode(), encryption_key).decode()
        number = Secure.encrypt(passport_num.encode(), encryption_key).decode()
        date = Secure.encrypt(issue_date.encode(), encryption_key).decode()
        authority = Secure.encrypt(issuing_authority.encode(), encryption_key).decode()

        cursor.execute(
            'SELECT username FROM passport_data '
            'WHERE passport_data.username = %s;', [self.username]
        )
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

        return True

    def retrieve(self) -> bool:
        """
        Load passport data into this object.

        :return: False if user not found, True on success
        """
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

    def get_data_without_db(self) -> Dict[str, str, str, str]:
        """
        Get passport data as dictionary.

        Available keys: passport_series, passport_number, issue_date, issuing_authority

        :return: Dictionary with data
        """
        return {
            'passport_series': self.passport_series, 'passport_number': self.passport_number,
            'issue_date': self.issue_date, 'issuing_authority': self.issuing_authority
        }


class Portfolio:
    """
    Model defines the Portfolio.
    """

    def __init__(self, username: str):
        """
        Create new Portfolio object.

        :param username: Portfolio owner username
        """
        self.conn = db_connect()
        self.username = username
        self.document = b'0'
        self.byte_count = 0

    def insert_file(self, document):
        """
        Insert user portfolio into database.

        :param document: Portfolio data
        :return: Just True
        """

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

        print('returned')
        return True

    def retrieve(self) -> Optional[Dict[str, int]]:
        """
        Retrieve the portfolio.

        :return: Dictionary with { attachment_integer: str, byte_count: int }
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT document FROM portfolios '
            'WHERE username = %s;',
            [self.username]
        )

        if cursor.rowcount == 0:
            return None

        record = next(cursor)
        cursor.close()
        print(record[0])
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
            # print(record)
            data = {
                'question': record[1],
                'choice1': record[2],
                'choice2': record[3],
                'choice3': record[4],
                'choice4': record[5]
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

    def insert_test(self, question: str, choice1: str, choice2: str, choice3: str, choice4: str):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO tests_questions (question, choice1, choice2, choice3, choice4) '
            'VALUES (%s, %s, %s, %s, %s);',
            (question, choice1, choice2, choice3, choice4)
        )
        self.conn.commit()
        cursor.close()
