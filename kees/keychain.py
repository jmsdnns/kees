import json
import os
import functools
from fuzzywuzzy import process

from kees.encryption import EncryptionKey


class UnlockException(Exception):
    pass

class KeyNotFoundException(Exception):
    pass


def load_encryption_keys(key_chain_path):
    path = os.path.join(key_chain_path, "data", "default", "encryptionKeys.js")
    with open(path, "r") as f:
        key_data = json.load(f)

    keys = {}
    for key_definition in key_data["list"]:
        key = EncryptionKey(**key_definition)
        keys[key.identifier] = key

    return keys


def load_item_list(key_chain_path):
    path = os.path.join(key_chain_path, "data", "default", "contents.js")
    with open(path, "r") as f:
        item_list = json.load(f)

    items = {}
    for item_definition in item_list:
        item = keychain_item_factory(item_definition, key_chain_path)
        items[item.name] = item

    return items


class Keychain(object):
    def __init__(self, path):
        self._locked = True
        self._path = os.path.expanduser(path)
        self._items = load_item_list(self._path)
        self._keys = load_encryption_keys(self._path)

    def locked(self):
        return self._locked

    def unlock(self, password):
        unlocker = lambda key: key.unlock(password)
        unlock_results = map(unlocker, self._keys.values())
        result = functools.reduce(lambda x, y: x and y, unlock_results)

        if not result:
            raise UnlockException("Password failure")
        self._locked = False

    def find_matches(self, match_str, fuzzy_threshold=100):
        matches = process.extract(match_str, self._items.keys())

        items = []
        for m in matches:
            if m[1] == 100:
                return [m]
            items.append(m)
        return items

    def get_key(self, identifier=None, security_level=None):
        if identifier and identifier in self._keys:
            key = self._keys[identifier]
            return key

        if security_level:
            for key in self._keys.values():
                if key.level == security_level:
                    return key

        err_msg = "Key not found for id:%s and level:%s"
        raise KeyNotFoundException(err_msg % (identifier, security_level))


def keychain_item_factory(row, path):
    identifier = row[0]
    type = row[1]
    name = row[2]

    item_type = KeychainItem
    if type == "webforms.WebForm":
        item_type = WebFormKeychainItem
    elif type == "passwords.Password":
        item_type = PasswordKeychainItem
    elif type == "wallet.onlineservices.GenericAccount":
        item_type = PasswordKeychainItem

    item = item_type(identifier, name, path, type)
    return item


class KeychainItem(object):
    def __init__(self, identifier, name, path, type):
        self.identifier = identifier
        self.name = name
        self.username = None
        self.password = None

        self._path = path
        self._type = type
        self._loaded = False

    def _load_file(self):
        filename = "%s.1password" % self.identifier
        path = os.path.join(self._path, "data", "default", filename)
        with open(path, "r") as f:
            item_data = json.load(f)

        self._key_identifier = item_data.get("keyID")
        self._security_level = item_data.get("securityLevel")
        if 'encrypted' in item_data:
            self._encrypted_json = item_data["encrypted"]

    def _find_password(self):
        err_msg = "Only use subclasses of KeychainItem"
        raise NotImplementedError(err_msg)

    def _find_username(self):
        err_msg = "Only use subclasses of KeychainItem"
        raise NotImplementedError(err_msg)

    @property
    def key_identifier(self):
        if not self._loaded:
            self._load_file()
        return self._key_identifier

    @property
    def security_level(self):
        if not self._loaded:
            self._load_file()
        return self._security_level

    def decrypt_with(self, keychain):
        key = keychain.get_key(
            identifier=self.key_identifier,
            security_level=self.security_level,
        )

        decrypted_json = key.decrypt(self._encrypted_json)
        decrypted_json = decrypted_json.strip(b'\x10')
        self._data = json.loads(decrypted_json)

        self.username = self._find_username()
        self.password = self._find_password()


class WebFormKeychainItem(KeychainItem):
    def _find_password(self):
        for field in self._data["fields"]:
            if field.get("designation") == "password":
                return field["value"]
            elif field.get("name") == "Password":
                return field["value"]
    def _find_username(self):
        for field in self._data["fields"]:
            if field.get("designation") == "username":
                return field["value"]
            elif field.get("name") == "Username":
                return field["value"]


class PasswordKeychainItem(KeychainItem):
    def _find_password(self):
        return self._data["password"]
    def _find_username(self):
        return self._data["username"]
