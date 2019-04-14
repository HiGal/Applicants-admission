import hashlib

import psycopg2

import SecretConstants
import Secure


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

    def verify(self):
        cursor = self.conn.cursor()
        password = self.password
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute('select * from sys_user where username = \'{}\' and password = \'{}\';'
                       .format(self.username, password))
        tmp = cursor.fetchall()
        if len(tmp) != 0:
            cursor.close()
            return True
        cursor.close()
        return False

    def register(self, username, password, name, sname, email, bdate):
        password = hashlib.md5(password.encode()).hexdigest()
        self.password = password
        self.username = username
        cursor = self.conn.cursor()
        cursor.execute(
            'insert into sys_user (username, password,name, surname, email,birthday) '
            'values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'
                .format(username, password, name, sname, email, bdate)
        )
        self.conn.commit()
        cursor.close()

    def contacts(self):
        cursor = self.conn.cursor()
        cursor.execute('select * from user_contact where uname=\'{}\';'.format(self.username))
        tmp = cursor.fetchall()
        if len(tmp) == 0:
            return None
        data = {
            'index': tmp[0][0],
            'region': tmp[0][1],
            'city': tmp[0][2],
            'street': tmp[0][3],
            'building': tmp[0][4],
            'corpus': tmp[0][5],
            'flat': tmp[0][6]
        }
        cursor.close()
        return data

    def update_contacts(self, index, region, city, street, building, corpus, flat):
        cursor = self.conn.cursor()
        cursor.execute('select * from user_contact where uname=\'{}\''.format(self.username))
        tmp = cursor.fetchall()
        if len(tmp) != 0:
            str = "update user_contact set index='%s', region='%s',city='%s',street='%s',building='%s',corpus='%s',flat='%s' where uname='%s';" \
                  % (index, region, city, street, building, corpus, flat, self.username)
            cursor.execute(str)
            self.conn.commit()
            cursor.close()
        else:
            str = "insert into user_contact (index,region,city,street,building,corpus,flat,uname)" \
                  " values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\','{}\',\'{}\')".format(index, region, city, street,
                                                                                            building, corpus, flat,
                                                                                            self.username)
            cursor.execute(str)
            self.conn.commit()
            cursor.close()

    def get_info(self):
        cursor = self.conn.cursor()
        # MAKE SURE THAT YOU DISABLED TESTING
        cursor.execute('select * from sys_user where username=\'{}\';'.format(self.username))
        tmp = cursor.fetchall()[0]
        data = {
            'name': tmp[2],
            'surname': tmp[3],
            'email': tmp[4],
            'birthday': tmp[5],
            'sex': tmp[6],
            'citizen': tmp[7]
        }
        return data

    def update_info(self, fname, sname, bdate, gender, citizenship):
        table_name = "sys_user"
        cursor = self.conn.cursor()

        str = "UPDATE %s SET name = '%s', surname = '%s', birthday='%s', sex='%s', citizen='%s' WHERE username = '%s';" \
              % (table_name, fname, sname, bdate, gender, citizenship, self.username)
        print(str)
        cursor.execute(str)
        self.conn.commit()
        cursor.close()


class PassportData:

    def __init__(self, username, passport_series=None, passport_number=None, issue_date=None,
                 issuing_authority=None):
        self.conn = db_connect()
        self.username = username
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.issue_date = issue_date
        self.issuing_authority = issuing_authority

    def register(self, passport_series: str, passport_num: str, issue_date: str, issuing_authority: str):
        encryption_key = Secure.create_key(SecretConstants.PASSPORT_ENCRYPTION_PASS,
                                           SecretConstants.PASSPORT_ENCRYPTION_SALT)

        series = Secure.encrypt(passport_series.encode(), encryption_key).decode()
        number = Secure.encrypt(passport_num.encode(), encryption_key).decode()
        date = Secure.encrypt(issue_date.encode(), encryption_key).decode()
        authority = Secure.encrypt(issuing_authority.encode(), encryption_key).decode()
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM passport_data WHERE passport_data.username = '%s';" % self.username)
        if cursor.rowcount != 0:
            cursor = self.conn.cursor()
            print("EMPTY HERE")
            cursor.execute(
                "UPDATE passport_data SET passport_series= '%s', passport_number= '%s', issue_date= '%s', issuing_authority='%s' where passport_data.username = '%s' " \
                % (series, number, date, authority, self.username)
            )
            self.conn.commit()
            cursor.close()
        else:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO passport_data (username, passport_series, passport_number, issue_date, issuing_authority) '
                'VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'
                    .format(self.username, series, number, date, authority)
            )
            self.conn.commit()
            cursor.close()

    def retrieve(self):
        cursor = self.conn.cursor()

        cursor.execute(
            'SELECT * FROM passport_data '
            'WHERE username=\'{}\';'.format(self.username)
        )

        if cursor.rowcount == 0:
            cursor.close()
            return False

        record = next(cursor)
        cursor.close()

        encryption_key = Secure.create_key(SecretConstants.PASSPORT_ENCRYPTION_PASS,
                                           SecretConstants.PASSPORT_ENCRYPTION_SALT)

        self.passport_series = Secure.decrypt(record[1].encode(), encryption_key).decode()
        self.passport_number = Secure.decrypt(record[2].encode(), encryption_key).decode()
        self.issue_date = Secure.decrypt(record[3].encode(), encryption_key).decode()
        self.issuing_authority = Secure.decrypt(record[4].encode(), encryption_key).decode()

        return True
