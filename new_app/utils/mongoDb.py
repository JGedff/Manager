from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure, NetworkTimeout, WriteError

from PyQt5.QtWidgets import QMessageBox

from utils.user_manager import UserManager
from utils.category import Category

class Mongo:
    _MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    _DB = _MONGO_CLIENT['manager']

    STORES_COLLECTION = _DB['stores']
    SPACES_COLLECTION = _DB['spaces']
    SHELVES_COLLECTION = _DB['shelfs']
    PRODUCTS_COLLECTION = _DB['products']
    CATEGORIES_COLLECTION = _DB['categorys']

    @classmethod
    def close_connection(cls):
        cls._MONGO_CLIENT.close()

    @classmethod
    def is_connection_open(cls):
        try:
            cls._MONGO_CLIENT.admin.command('ping')
            return True
        except Exception:
            return False
        
    @classmethod
    def reconnect(cls):
        cls._MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

        cls._DB = cls._MONGO_CLIENT['manager']
        cls.STORES_COLLECTION = cls._DB['stores']
        cls.SPACES_COLLECTION = cls._DB['spaces']
        cls.SHELVES_COLLECTION = cls._DB['shelfs']
        cls.PRODUCTS_COLLECTION = cls._DB['products']
        cls.CATEGORIES_COLLECTION = cls._DB['categorys']

    @classmethod
    def add_shelves(cls, shelves = []):
        insert_shelves = []

        for local_shelf in shelves:
            insert_shelf = {
                "floors": local_shelf['floors'],
                "spaces": [],
                "double_shelf": local_shelf['double_shelf'],
                "creation_date": str(datetime.now())[:-3]
            }

            try:
                cls.SPACES_COLLECTION.insert_many(local_shelf['spaces'])
            except (ConnectionFailure, ServerSelectionTimeoutError):
                UserManager.set_user('Guest', 'Offline')
                QMessageBox.warning(None, "The spaces were not created", "There was an issue with the network")
                break

            insert_shelf['spaces'] = cls.get_last_spaces_created(len(local_shelf['spaces']))

            insert_shelves.append(insert_shelf)

        try:
            cls.SHELVES_COLLECTION.insert_many(insert_shelves)
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The shelves were not created", "There was an issue with the network")

    @classmethod
    def get_last_spaces_created(cls, num):
        spaces = []

        try:
            db_spaces = cls.SPACES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

            for mongo_space in db_spaces:
                spaces.append(mongo_space['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Spaces not found", "There was an issue with the network")

        return spaces

    @classmethod
    def get_last_shelves_created(cls, num):
        shelves = []

        try: 
            db_shelves = cls.SHELVES_COLLECTION.find({}).sort([('creation_date', -1)]).limit(num)

            for mongo_shelf in db_shelves:
                shelves.insert(0, mongo_shelf['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Shelves not found", "There was an issue with the network")

        return shelves

    @classmethod
    def add_store(cls, shelves, name, image):
        cls.add_shelves(shelves)

        id_shelves = cls.get_last_shelves_created(len(shelves))

        max_floor = 0

        for shelf in shelves:
            if shelf['floors'] > max_floor:
                max_floor = shelf['floors']

        try:
            cls.STORES_COLLECTION.insert_one({ "name": name, "image": image, "storeShelves": id_shelves, "storeFloors": max_floor })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The store was not created", "There was an issue with the network")

    @classmethod
    def get_category_by_name(cls, name):
        try:
            file = cls.CATEGORIES_COLLECTION.find_one({ "name": name })

            return file['_id']
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return name

    @classmethod
    def update_category_space(cls, space_id, category_name = None):
        if space_id != None:
            category_id = cls.get_category_by_name(category_name)

            try:
                cls.SPACES_COLLECTION.update_one({ "mongo_id": space_id }, { "$set": { "category": category_id } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
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
        categoryId = cls.get_category_by_name(category)

        try:
            cls.CATEGORIES_COLLECTION.update_one({ "_id": categoryId }, { "$set": { "hold": holdsProduct } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def get_products(cls) -> list:
        try:
            products = []

            for db_product in cls.PRODUCTS_COLLECTION.find({}):
                products.append({ "name": db_product['name'].capitalize(), "price": db_product['price'] })

            return products

        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Products not found", "There was an issue with the network")

            return []
    
    @classmethod
    def add_product(cls, product_name: str, price: float):
        try:
            cls.PRODUCTS_COLLECTION.insert_one({
                "name": product_name.lower(),
                "price": price
            })

        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The product was not created", "There was an issue with the network")

    @classmethod
    def update_space_amount(cls, space_id, amount: int):
        if space_id != None:
            try:
                cls.SPACES_COLLECTION.update_one({ "mongo_id": space_id }, { "$set": { "amount": amount } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
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
    def update_space_product(cls, space_id, new_product):
        if space_id != None:
            try:
                if new_product != '':
                    productId = cls.getMongoProductByName(new_product)

                    if productId != None:
                        cls.SPACES_COLLECTION.update_one({ "mongo_id": space_id }, { "$set": { "product": productId } })
                    else:
                        QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
                else:
                    cls.SPACES_COLLECTION.update_one({ "mongo_id": space_id }, { "$unset": { "product": "" } })

            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
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
    def del_product(cls, prduct_name: str):
        try:
            cls.PRODUCTS_COLLECTION.delete_one({ "name": prduct_name.lower() })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
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

                create_category_in(shortcut_category, category['name'], widget)
                mongoCategories += 1
            
            mongoConnection = True

            update_category_buttons_pos(shortcut_category)
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

            create_category_in(shortcut_category, 'Empty', widget)
            create_category_in(shortcut_category, 'Unreachable', widget)
            create_category_in(shortcut_category, 'Fill', widget)
            update_category_buttons_pos(shortcut_category)

        elif mongoCategories <= 0:
            QMessageBox.warning(None, "You don't have connection to the database", "You'll use the default categories")

            Category.add_category('Empty', 'white')
            Category.add_category('Unreachable', 'red')
            Category.add_category('Fill', 'green')
            Category.change_can_hold_product('Fill', True)

            create_category_in(shortcut_category, 'Empty', widget)
            create_category_in(shortcut_category, 'Unreachable', widget)
            create_category_in(shortcut_category, 'Fill', widget)
            update_category_buttons_pos(shortcut_category)
            
        set_empty_category(shortcut_category)

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
                
                save_shelves_info(SHELVES_FORMS)
                
                Store.createStore(store['name'], widget, store['image'])

                STORES[store_index].goBackStore.hide()

                for shelfIndex in range(store['storeShelves'].__len__()):
                    for index, mongoSpace in enumerate(spacesInfo[shelfIndex]):
                        SHELVES[store_index][shelfIndex].spaces[index].mongo_id = mongoSpace['mongo_id']

                        if mongoCategories > 0:
                            category = Mongo.CATEGORIES_COLLECTION.find_one({ "_id": mongoSpace['category'] })

                            if category != None:
                                SHELVES[store_index][shelfIndex].spaces[index].category_selector.setCurrentText(category['name'])
                                SHELVES[store_index][shelfIndex].spaces[index].category.name = category['name']
                                SHELVES[store_index][shelfIndex].spaces[index].category.color = category['color']

                                if isinstance(SHELVES[store_index][shelfIndex].spaces[index].product, Product):
                                    SHELVES[store_index][shelfIndex].spaces[index].product.hide()
                
                store_index =+ 1
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.warning(None, "Network error", "There was an issue with the network")
