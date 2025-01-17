from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure, NetworkTimeout, WriteError

from PyQt5.QtWidgets import QMessageBox

from utils.user_manager import UserManager
from utils.category import Category

class Mongo:
    MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    DB = MONGO_CLIENT['manager']

    STORES_COLLECTION = DB['stores']
    SPACES_COLLECTION = DB['spaces']
    SHELVES_COLLECTION = DB['shelfs']
    PRODUCTS_COLLECTION = DB['products']
    CATEGORIES_COLLECTION = DB['categorys']

    @staticmethod
    def closeMongoConnection():
        Mongo.MONGO_CLIENT.close()

    @staticmethod
    def connectionIsOpen():
        try:
            Mongo.MONGO_CLIENT.admin.command('ping')
            return True
        except Exception:
            return False
        
    @staticmethod
    def reconnect():
        Mongo.MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

        Mongo.DB = Mongo.MONGO_CLIENT['manager']
        Mongo.STORES_COLLECTION = Mongo.DB['stores']
        Mongo.SPACES_COLLECTION = Mongo.DB['spaces']
        Mongo.SHELVES_COLLECTION = Mongo.DB['shelfs']
        Mongo.PRODUCTS_COLLECTION = Mongo.DB['products']
        Mongo.CATEGORIES_COLLECTION = Mongo.DB['categorys']

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
                UserManager.setUser('Guest', 'Offline')
                QMessageBox.warning(None, "The spaces were not created", "There was an issue with the network")
                break

            insertShelf['spaces'] = cls.getLastSpacesCreated(shelves['spaces'].__len__())

            arrayToInsert.append(insertShelf)

        try:
            cls.SHELVES_COLLECTION.insert_many(arrayToInsert)
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The shelves were not created", "There was an issue with the network")

    @classmethod
    def getLastSpacesCreated(cls, num):
        spacesId = []

        try:
            lastSpaces = cls.SPACES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

            for doc in lastSpaces:
                spacesId.append(doc['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
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
            UserManager.setUser('Guest', 'Offline')
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
            UserManager.setUser('Guest', 'Offline')
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
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return name

    @classmethod
    def updateMongoSpaceCategory(cls, spaceId, category, oldName = None):
        if spaceId != None:
            categoryId = cls.getMongoCategoryByName(category, oldName)

            try:
                cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "category": categoryId } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.setUser('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoCategoryName(cls, oldName, newName):
        try:
            cls.CATEGORIES_COLLECTION.update_one({ "name": oldName }, { "$set": { "name": newName } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoCategoryColor(cls, name, color):
        try:
            cls.CATEGORIES_COLLECTION.update_one({ "name": name }, { "$set": { "color": color } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def delMongoCategory(cls, name):
        try:
            cls.CATEGORIES_COLLECTION.delete_one({ "name": name })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The user was not deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the user", f"Write error: {e.details}")

    @classmethod
    def addMongoCategory(cls, name, color, canHoldProduct):
        try:
            cls.CATEGORIES_COLLECTION.insert_one({
                "name": name,
                "color": color,
                "hold": canHoldProduct
            })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not created", "There was an issue with the network")

    @classmethod
    def updateMongoCategoryHoldsProducts(cls, category, holdsProduct):
        categoryId = cls.getMongoCategoryByName(category, category)

        try:
            cls.CATEGORIES_COLLECTION.update_one({ "_id": categoryId }, { "$set": { "hold": holdsProduct } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def getMongoProducts(cls):
        try:
            allProducts = []

            for product in cls.PRODUCTS_COLLECTION.find({}):
                allProducts.append({ "name": product['name'].capitalize(), "price": product['price'] })

            return allProducts
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "Products not found", "There was an issue with the network")

            return []
    
    @classmethod
    def addMongoProducts(cls, name, price):
        try:
            cls.PRODUCTS_COLLECTION.insert_one({
                "name": name.lower(),
                "price": price
            })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The product was not created", "There was an issue with the network")

    @classmethod
    def updateMongoSpaceAmount(cls, spaceId, amount):
        if spaceId != None:
            try:
                cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "amount": amount } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.setUser('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def getMongoProductByName(cls, nameProduct):
        try:
            file = cls.PRODUCTS_COLLECTION.find_one({ "name": nameProduct.lower() })

            return file['_id']
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return None

    @classmethod
    def updateMongoSpaceProduct(cls, spaceId, newProduct):
        if spaceId != None:
            try:
                if newProduct != '':
                    productId = cls.getMongoProductByName(newProduct)

                    if productId != None:
                        cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$set": { "product": productId } })
                    else:
                        QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
                else:
                    cls.SPACES_COLLECTION.update_one({ "mongo_id": spaceId }, { "$unset": { "product": "" } })

            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.setUser('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoProduct(cls, oldName, newName, newPrice):
        try:
            productId = cls.getMongoProductByName(oldName)

            if productId != None:
                cls.PRODUCTS_COLLECTION.update_one({ "_id": productId }, { "$set": { "name": newName.lower(), "price": newPrice } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoProductName(cls, oldName, newName):
        try:
            productId = cls.getMongoProductByName(oldName)

            if productId != None:
                cls.PRODUCTS_COLLECTION.update_one({ "_id": productId }, { "$set": { "name": newName.lower() } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def updateMongoProductPrice(cls, oldName, newPrice):
        try:
            productId = cls.getMongoProductByName(oldName)

            if productId != None:
                cls.PRODUCTS_COLLECTION.update_one({ "_id": productId }, { "$set": { "price": newPrice } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def delMongoProduct(cls, name):
        try:
            cls.PRODUCTS_COLLECTION.delete_one({ "name": name.lower() })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The product was not deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the product", f"Write error: {e.details}")

    @classmethod
    def get_mongo_info(widget, shortcut_category):
        store_index = 0
        mongoCategories = 0
        mongoConnection = False

        try:
            for category in Mongo.CATEGORIES_COLLECTION.find({}):
                Category.add_category(category['name'], category['color'])
                Category.change_can_hold_product(category['name'], category['hold'])

                createCategoryIn(shortcut_category, category['name'], widget, True)
                mongoCategories += 1
            
            mongoConnection = True

            updateButtonsPosition(shortcut_category, True)
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')

            QMessageBox.warning(None, "Categories not found", "There was an issue with the network")

            mongoCategories = 0

        if mongoConnection and mongoCategories <= 0:
            QMessageBox.warning(None, "There aren't any categories in the database", "The default categories will be created")

            Mongo.addMongoCategory('Empty', 'white', False)
            Mongo.addMongoCategory('Unreachable', 'red', False)
            Mongo.addMongoCategory('Fill', 'green', True)

            Category.add_category('Empty', 'white')
            Category.add_category('Unreachable', 'red')
            Category.add_category('Fill', 'green')
            Category.change_can_hold_product('Fill', True)

            createCategoryIn(shortcut_category, 'Empty', widget, True)
            createCategoryIn(shortcut_category, 'Unreachable', widget, True)
            createCategoryIn(shortcut_category, 'Fill', widget, True)
            updateButtonsPosition(shortcut_category, True)

        elif mongoCategories <= 0:
            QMessageBox.warning(None, "You don't have connection to the database", "You'll use the default categories")

            Category.add_category('Empty', 'white')
            Category.add_category('Unreachable', 'red')
            Category.add_category('Fill', 'green')
            Category.change_can_hold_product('Fill', True)

            createCategoryIn(shortcut_category, 'Empty', widget, True)
            createCategoryIn(shortcut_category, 'Unreachable', widget, True)
            createCategoryIn(shortcut_category, 'Fill', widget, True)
            updateButtonsPosition(shortcut_category, True)
            
        setEmptyCategory(shortcut_category)

        try:
            for store in Mongo.STORES_COLLECTION.find({}):
                spacesInfo = []

                for index, shelf_id in enumerate(store['storeShelves']):
                    shelf = Mongo.SHELVES_COLLECTION.find_one({ "_id": shelf_id })
                    mongoSpaces = Mongo.SPACES_COLLECTION.find({"_id": {"$in": shelf['spaces']}})
                    
                    Shelf.createShelf(widget)

                    SHELVES_FORMS[index].input_spaces.set_value(shelf['spaces'].__len__() / store['storeFloors'])
                    SHELVES_FORMS[index].input_shelf_floors.set_value(shelf['floors'])
                    SHELVES_FORMS[index].double_shelf_input.set_value(shelf['double_shelf'])
                    SHELVES_FORMS[index].hideForm()

                    spacesInfo.append(mongoSpaces)
                
                saveShelfInfo(SHELVES_FORMS)
                
                Store.createStore(store['name'], widget, store['image'])

                STORES[store_index].goBackStore.hide()

                for shelfIndex in range(store['storeShelves'].__len__()):
                    for index, mongoSpace in enumerate(spacesInfo[shelfIndex]):
                        SHELVES[store_index][shelfIndex].spaces[index].mongo_id = mongoSpace['mongo_id']

                        if mongoCategories > 0:
                            category = Mongo.CATEGORIES_COLLECTION.find_one({ "_id": mongoSpace['category'] })

                            if category != None:
                                SHELVES[store_index][shelfIndex].spaces[index].categorySelector.setCurrentText(category['name'])
                                SHELVES[store_index][shelfIndex].spaces[index].category.name = category['name']
                                SHELVES[store_index][shelfIndex].spaces[index].category.color = category['color']

                                if isinstance(SHELVES[store_index][shelfIndex].spaces[index].product, Product):
                                    SHELVES[store_index][shelfIndex].spaces[index].product.hide()
                
                store_index =+ 1
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "Network error", "There was an issue with the network")
