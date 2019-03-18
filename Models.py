import psycopg2


class User:

    def __init__(self, username=None, password=None):
        self.conn = psycopg2.connect(dbname='appadmission', user='team7',
                                     password='123', host='localhost')
        self.username = username
        self.password = password

    def verify(self):
        cursor = self.conn.cursor()
        cursor.execute('select * from sys_user where username = \'{}\' and password = \'{}\''
                       .format(self.username, self.password))
        tmp = cursor.fetchall()
        if len(tmp) != 0:
            cursor.close()
            return True
        cursor.close()
        return False

    def register(self, username, password, name, sname, email, bdate):
        cursor = self.conn.cursor()
        cursor.execute('insert into sys_user (username, password,name, sname, email,birthday) '
                       'values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'
                       .format(username, password, name, sname, email, bdate))
        self.conn.commit()
        cursor.close()
