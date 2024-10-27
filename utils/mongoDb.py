from datetime import datetime

from pymongo import MongoClient

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

            cls.SPACES_COLLECTION.insert_many(shelves['spaces'])

            insertShelf['spaces'] = cls.getLastSpacesCreated(shelves['spaces'].__len__())

            arrayToInsert.append(insertShelf)

        cls.SHELVES_COLLECTION.insert_many(arrayToInsert)

    @classmethod
    def getLastSpacesCreated(cls, num):
        spacesId = []

        lastSpaces = cls.SPACES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

        for doc in lastSpaces:
            spacesId.append(doc['_id'])

        return spacesId

    @classmethod
    def getLastShelvesCreated(cls, num):
        shelvesId = []

        lastShelves = cls.SHELVES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

        for doc in lastShelves:
            shelvesId.insert(0, doc['_id'])

        return shelvesId

    @classmethod
    def addStoreToMongo(cls, arrayShelves, name, image):
        cls.addShelvesToMongo(arrayShelves)

        idNewShelves = cls.getLastShelvesCreated(arrayShelves.__len__())

        maxFloor = 0

        for shelf in arrayShelves:
            if shelf['floors'] > maxFloor:
                maxFloor = shelf['floors']

        cls.STORES_COLLECTION.insert_one({ "name": name, "image": image, "storeShelves": idNewShelves, "storeFloors": maxFloor })

    @classmethod
    def getMongoCategoryByName(cls, name, oldName):
        file = cls.CATEGORIES_COLLECTION.find_one({ "name": name })

        if file: return file['_id']
        else:
            file = cls.CATEGORIES_COLLECTION.find_one({ "name": oldName })

            return file['_id']

    @classmethod
    def updateMongoSpaceCategory(cls, spaceId, category, oldName = None):
        if spaceId != None:
            categoryId = cls.getMongoCategoryByName(category, oldName)

            cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "category": categoryId } })

    @classmethod
    def updateMongoCategoryName(cls, oldName, newName):
        cls.CATEGORIES_COLLECTION.update_one({ "name": oldName }, { "$set": { "name": newName } })

    @classmethod
    def updateMongoCategoryColor(cls, name, color):
        cls.CATEGORIES_COLLECTION.update_one({ "name": name }, { "$set": { "color": color } })

    @classmethod
    def delMongoCategory(cls, name):
        cls.CATEGORIES_COLLECTION.delete_one({ "name": name })

    @classmethod
    def addMongoCategory(cls, name, color):
        cls.CATEGORIES_COLLECTION.insert_one({
            "name": name,
            "color": color
        })
