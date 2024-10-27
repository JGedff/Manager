from datetime import datetime

from pymongo import MongoClient

MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

DB = MONGO_CLIENT['manager']

STORES_COLLECTION = DB['stores']
SPACES_COLLECTION = DB['spaces']
SHELVES_COLLECTION = DB['shelfs']
CATEGORIES_COLLECTION = DB['categorys']

def closeMongoConnection():
    MONGO_CLIENT.close()

def addShelvesToMongo(arrayInfo = []):
    arrayToInsert = []

    for shelves in arrayInfo:
        insertShelf = {
            "floors": shelves['floors'],
            "spaces": [],
            "double_shelf": shelves['double_shelf'],
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        }

        SPACES_COLLECTION.insert_many(shelves['spaces'])

        insertShelf['spaces'] = getLastSpacesCreated(shelves['spaces'].__len__())

        arrayToInsert.append(insertShelf)

    SHELVES_COLLECTION.insert_many(arrayToInsert)

def getLastSpacesCreated(num):
    spacesId = []

    lastSpaces = SPACES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

    for doc in lastSpaces:
        spacesId.append(doc['_id'])

    return spacesId

def getLastShelvesCreated(num):
    shelvesId = []

    lastShelves = SHELVES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

    for doc in lastShelves:
        shelvesId.insert(0, doc['_id'])

    return shelvesId

def addStoreToMongo(arrayShelves, name, image):
    addShelvesToMongo(arrayShelves)

    idNewShelves = getLastShelvesCreated(arrayShelves.__len__())

    maxFloor = 0

    for shelf in arrayShelves:
        if shelf['floors'] > maxFloor:
            maxFloor = shelf['floors']

    STORES_COLLECTION.insert_one({ "name": name, "image": image, "storeShelves": idNewShelves, "storeFloors": maxFloor })

def getMongoCategoryByName(name, oldName):
    file = CATEGORIES_COLLECTION.find_one({ "name": name })

    if file: return file['_id']
    else:
        file = CATEGORIES_COLLECTION.find_one({ "name": oldName })

        return file['_id']

def updateMongoSpaceCategory(spaceId, category, oldName = None):
    if spaceId != None:
        categoryId = getMongoCategoryByName(category, oldName)

        SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "category": categoryId } })

def updateMongoCategoryName(oldName, newName):
    CATEGORIES_COLLECTION.update_one({ "name": oldName }, { "$set": { "name": newName } })

def updateMongoCategoryColor(name, color):
    CATEGORIES_COLLECTION.update_one({ "name": name }, { "$set": { "color": color } })

def delMongoCategory(name):
    CATEGORIES_COLLECTION.delete_one({ "name": name })

def addMongoCategory(name, color):
    CATEGORIES_COLLECTION.insert_one({
        "name": name,
        "color": color
    })