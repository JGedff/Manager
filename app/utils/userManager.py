from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout, WriteError, InvalidDocument
from pymongo import MongoClient

from PyQt5.QtWidgets import QMessageBox

from utils.encrypt import Encrypt

class UserManager:
    MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    DB = MONGO_CLIENT['manager']

    USERS_COLLECTION = DB['users']

    username = ''
    role = ''

    @classmethod
    def register(cls, username, password):
        try:
            [user, _] = cls.findUser(username)

            if user == 'New':
                cls.USERS_COLLECTION.insert_one({
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
    def authenticate(cls, username, password):
        try:
            user = cls.USERS_COLLECTION.find_one({ "username": username })
            
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
            cls.USERS_COLLECTION.delete_one({ "username": username })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "The user was deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the user", f"Write error: {e.details}")

    @classmethod
    def findUser(cls, username):
        try:
            user = cls.USERS_COLLECTION.find_one({ "username": username })

            return [user['username'], user['role']]
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            return ['Guest', 'Offline']
        except InvalidDocument:
            return ['Guest', 'Offline']
        except TypeError:
            return ['New', 'User']
        
    @classmethod
    def setUser(cls, username, role):
        cls.username = username
        cls.role = role

    @classmethod
    def getUserRole(cls):
        return cls.role
