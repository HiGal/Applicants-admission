import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key(password: bytes, salt: bytes, length: int = 32) -> bytes:
	"""
	Creates a key for encryption.

	:param password: Encryption password in bytes
	:param salt: Encryption salt in bytes
	:param length: Desired key length (default is 32)
	:return: Encryption key in bytes
	"""
	if len(salt) < 16:
		raise ValueError('Salt should be 16-byte or longer, but it was {} byte.'.format(len(salt)))

	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA3_256,
		length=length,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)

	return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt(data: bytes, key: bytes) -> bytes:
	"""
	Encrypts the data.

	:param data: Data in bytes
	:param key: Key in bytes
	:return: Encrypted data in bytes.
	"""
	fernet = Fernet(key)
	return fernet.encrypt(data)


def decrypt(data: bytes, key: bytes) -> bytes:
	"""
	Decrypts the data.

	:param data: Encrypted data in bytes.
	:param key: Key in bytes.
	:return: Source data in bytes.
	"""
	fernet = Fernet(key)
	return fernet.decrypt(data)
