from base64 import b64decode
from hashlib import md5
from M2Crypto import EVP


def aes_decrypt(key, iv, encrypted_data):
    aes = EVP.Cipher(
        "aes_128_cbc", key, iv, key_as_bytes=False, padding=False, op=0
    )
    v = aes.update(encrypted_data) + aes.final()
    return strip_padding(v)


def strip_padding(decrypted):
    padding_size = decrypted[-1]
    if padding_size >= 16:
        return decrypted
    else:
        return decrypted[:-padding_size]


def derive_pbkdf2(password, salt, iterations):
    key_and_iv = EVP.pbkdf2(password, salt, iterations, 32)
    return key_and_iv[0:16], key_and_iv[16:]


def derive_openssl(key, salt):
    key = key[0:-16]
    key_and_iv = bytes()
    prev = bytes()
    while len(key_and_iv) < 32:
        hash_bytes = prev + key + salt
        prev = md5(hash_bytes).digest()
        key_and_iv += prev

    return key_and_iv[0:16], key_and_iv[16:]
    


SALTED_PREFIX = b'Salted__'
ZERO_INIT_VECTOR = b'\x00' * 16

def extract_salt(base64_encoded_string):
    decoded_data = b64decode(base64_encoded_string)

    if decoded_data.startswith(SALTED_PREFIX):
        salt = decoded_data[8:16]
        data = decoded_data[16:]
    else:
        salt = ZERO_INIT_VECTOR
        data = decoded_data

    return salt, data


class EncryptionKey(object):
    MINIMUM_ITERATIONS = 1000

    def __init__(
        self, data, iterations=0, validation="", identifier=None, level=None
    ):
        iterations = max(int(iterations), self.MINIMUM_ITERATIONS)
        salt, key = extract_salt(data)

        self.identifier = identifier
        self.iterations = iterations
        self.level = level

        self._encrypted_key = key
        self._salt = salt
        self._decrypted_key = None
        self._validation = validation

    def unlock(self, password):
        key, iv = derive_pbkdf2(
            password, self._salt, self.iterations
        )

        self._decrypted_key = aes_decrypt(
            key=key,
            iv=iv,
            encrypted_data=self._encrypted_key,
        )

        return self.decrypt(self._validation) == self._decrypted_key

    def decrypt(self, b64_data):
        salt, data = extract_salt(b64_data)
        key, iv = derive_openssl(self._decrypted_key, salt)
        return aes_decrypt(key=key, iv=iv, encrypted_data=data)

