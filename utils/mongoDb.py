from pymongo import MongoClient

MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

DB = MONGO_CLIENT['manager']

STORES_COLLECTION = DB['stores']
SHELVES_COLLECTION = DB['shelfs']
CATEGORIES_COLLECTION = DB['categorys']

def closeMongoConnection():
    MONGO_CLIENT.close()

def addShelvesToMongo(arrayInfo = []):
    SHELVES_COLLECTION.insert_many(arrayInfo)

def getLastShelvesCreated(num):
    shelvesId = []

    lastShelves = SHELVES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

    for doc in lastShelves:
        shelvesId.append(doc['_id'])

    return shelvesId

def addStoreToMongo(arrayShelves, name, image):
    addShelvesToMongo(arrayShelves)

    idNewShelves = getLastShelvesCreated(arrayShelves.__len__())

    STORES_COLLECTION.insert_one({ "name": name, "image": image, "storeShelves": idNewShelves })

def getMongoCategoryByName(name):
    file = CATEGORIES_COLLECTION.find_one({ "name": name })

    return file['_id']