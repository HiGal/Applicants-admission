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
		password = hashlib.md5(self.password.encode()).hexdigest()
		# print(password)
		cursor.execute('select * from sys_user where username = \'{}\' and password = \'{}\''
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
		cursor.execute(
			'insert into sys_user (username, password,name, surname, email,birthday) '
			'values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'
				.format(username, password, name, sname, email, bdate)
		)
		self.conn.commit()
		cursor.close()


class PassportData:
	def __init__(self, username, passport_series=None, passport_num=None, issue_date=None, issuing_authority=None):
		self.conn = db_connect()
		self.username = username
		self.passport_series = passport_series
		self.passport_num = passport_num
		self.issue_date = issue_date
		self.issuing_authority = issuing_authority

	def register(self, username: str, passport_series: str, passport_num: str, issue_date: str, issuing_authority: str):
		encryption_key = Secure.create_key(SecretConstants.PASSPORT_ENCRYPTION_PASS,
		                                   SecretConstants.PASSPORT_ENCRYPTION_SALT)

		series = Secure.encrypt(passport_series.encode(), encryption_key)
		number = Secure.encrypt(passport_num.encode(), encryption_key)
		date = Secure.encrypt(issue_date.encode(), encryption_key)
		authority = Secure.encrypt(issuing_authority.encode(), encryption_key)

		cursor = self.conn.cursor()
		cursor.execute(
			'INSERT INTO passport_data (username, passport_series, passport_number, issue_date, issuing_authority) '
			'VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'
				.format(username, series, number, date, authority)
		)
		self.conn.commit()
		cursor.close()
