from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout, WriteError, InvalidDocument

from PyQt5.QtWidgets import QMessageBox

from utils.db import DB
from utils.encrypt import Encrypt

class UserManager:
    _username = ''
    _role = ''

    @classmethod
    def register(cls, username, password) -> str:
        try:
            user = cls.is_duplicated(username)

            if not user:
                DB.insert_one_user({
                    "username": username,
                    "password": Encrypt.hash(password),
                    "role": "User"
                })
            else:
                return 'Duplicated'
        except (ConnectionFailure, ServerSelectionTimeoutError):
            QMessageBox.warning(None, "The user was not created", "There was an issue with the network")

            return 'NoInternet'
        except DuplicateKeyError:
            return 'Duplicated'
        
        return username

    @classmethod
    def authenticate(cls, username, password) -> str | None:
        try:
            user = DB.get_one_user({ "username": username })

            if user != None:

                if Encrypt.check(user['password'], password):
                    return user['role']
                else:
                    return None
            else:
                return user
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            return 'NoInternet'
        except InvalidDocument:
            return None

    @classmethod
    def delete(cls, username):
        try:
            DB.delete_one_user({ "username": username })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "The user was deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the user", f"Write error: {e.details}")

    @classmethod
    def is_duplicated(cls, username) -> bool:
        try:
            user = DB.get_one_user({ "username": username })

            return user != None
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            return True
        except InvalidDocument:
            return True
        except TypeError:
            return False
    
    @classmethod
    def find_user_role(cls, username) -> str:
        try:
            user = DB.get_one_user({ "username": username })

            return user['role']
        except:
            return 'Offline'

    @classmethod
    def set_user(cls, username, role):
        cls._username = username
        cls._role = role

    @classmethod
    def get_role(cls) -> str:
        return cls._role

    @classmethod
    def get_username(cls) -> str:
        return cls._username
