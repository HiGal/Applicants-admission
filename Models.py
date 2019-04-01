import psycopg2
import hashlib


class User:

    def __init__(self, username=None, password=None):
        self.conn = psycopg2.connect(dbname='ddlnar37d92bn9', user='nmlgmsljgwxbma',
                                     password='c97f630d0d9f0497070fb3f8e1468a1e742d190d2a5d8366d484d3c21bf8d5a9',
                                     host='ec2-107-20-177-161.compute-1.amazonaws.com')
        self.username = username
        self.password = password

    def verify(self):
        cursor = self.conn.cursor()
        password = hashlib.md5(self.password.encode()).hexdigest()
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
        cursor = self.conn.cursor()
        cursor.execute('insert into sys_user (username, password,name, surname, email,birthday) '
                       'values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'
                       .format(username, password, name, sname, email, bdate))
        self.conn.commit()
        cursor.close()

    def contacts(self):
        cursor = self.conn.cursor()
        cursor.execute('select * from user_contact where uname=\'{}\';'.format(self.username))
        tmp = cursor.fetchall()
        data = {
            'index': tmp[0][0],
            'region': tmp[0][1],
            'city': tmp[0][2],
            'street': tmp[0][3],
            'building': tmp[0][4],
            'corpus': tmp[0][5],
            'flat': tmp[0][6]
        }
        return data
