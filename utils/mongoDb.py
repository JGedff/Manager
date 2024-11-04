from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure, NetworkTimeout, WriteError

from PyQt5.QtWidgets import QMessageBox

class Mongo:
    MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    DB = MONGO_CLIENT['manager']

    STORES_COLLECTION = DB['stores']
    SPACES_COLLECTION = DB['spaces']
    SHELVES_COLLECTION = DB['shelfs']
    CATEGORIES_COLLECTION = DB['categorys']

    @staticmethod
    def closeMongoConnection():
        Mongo.MONGO_CLIENT.close()

    @classmethod
    def addShelvesToMongo(cls, arrayInfo = []):
        arrayToInsert = []

        for shelves in arrayInfo:
            insertShelf = {
                "floors": shelves['floors'],
                "spaces": [],
                "double_shelf": shelves['double_shelf'],
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            }

            try:
                cls.SPACES_COLLECTION.insert_many(shelves['spaces'])
            except (ConnectionFailure, ServerSelectionTimeoutError):
                QMessageBox.warning(None, "The spaces were not created", "There was an issue with the network")
                break

            insertShelf['spaces'] = cls.getLastSpacesCreated(shelves['spaces'].__len__())

            arrayToInsert.append(insertShelf)

        try:
            cls.SHELVES_COLLECTION.insert_many(arrayToInsert)
        except (ConnectionFailure, ServerSelectionTimeoutError):
            QMessageBox.warning(None, "The shelves were not created", "There was an issue with the network")

    @classmethod
    def getLastSpacesCreated(cls, num):
        spacesId = []

        try:
            lastSpaces = cls.SPACES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

            for doc in lastSpaces:
                spacesId.append(doc['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "Spaces not found", "There was an issue with the network")

        return spacesId

    @classmethod
    def getLastShelvesCreated(cls, num):
        shelvesId = []

        try: 
            lastShelves = cls.SHELVES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

            for doc in lastShelves:
                shelvesId.insert(0, doc['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "Shelves not found", "There was an issue with the network")

        return shelvesId

    @classmethod
    def addStoreToMongo(cls, arrayShelves, name, image):
        cls.addShelvesToMongo(arrayShelves)

        idNewShelves = cls.getLastShelvesCreated(arrayShelves.__len__())

        maxFloor = 0

        for shelf in arrayShelves:
            if shelf['floors'] > maxFloor:
                maxFloor = shelf['floors']

        try:
            cls.STORES_COLLECTION.insert_one({ "name": name, "image": image, "storeShelves": idNewShelves, "storeFloors": maxFloor })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            QMessageBox.warning(None, "The store was not created", "There was an issue with the network")

    @classmethod
    def getMongoCategoryByName(cls, name, oldName):
        try:
            file = cls.CATEGORIES_COLLECTION.find_one({ "name": name })

            if file: return file['_id']
            else:
                file = cls.CATEGORIES_COLLECTION.find_one({ "name": oldName })

                return file['_id']
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return name

    @classmethod
    def updateMongoSpaceCategory(cls, spaceId, category, oldName = None):
        if spaceId != None:
            categoryId = cls.getMongoCategoryByName(category, oldName)

            try:
                cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "category": categoryId } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoCategoryName(cls, oldName, newName):
        try:
            cls.CATEGORIES_COLLECTION.update_one({ "name": oldName }, { "$set": { "name": newName } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoCategoryColor(cls, name, color):
        try:
            cls.CATEGORIES_COLLECTION.update_one({ "name": name }, { "$set": { "color": color } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def delMongoCategory(cls, name):
        try:
            cls.CATEGORIES_COLLECTION.delete_one({ "name": name })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            QMessageBox.warning(None, "The user was deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the user", f"Write error: {e.details}")


    @classmethod
    def addMongoCategory(cls, name, color):
        try:
            cls.CATEGORIES_COLLECTION.insert_one({
                "name": name,
                "color": color
            })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            QMessageBox.warning(None, "The category was not created", "There was an issue with the network")
