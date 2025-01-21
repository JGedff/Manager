from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure, NetworkTimeout, WriteError

from PyQt5.QtWidgets import QMessageBox

from utils.user_manager import UserManager

class Mongo:
    _MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    _DB = _MONGO_CLIENT['manager']

    _STORES_COLLECTION = _DB['stores']
    _SPACES_COLLECTION = _DB['spaces']
    _SHELVES_COLLECTION = _DB['shelfs']
    _PRODUCTS_COLLECTION = _DB['products']
    _CATEGORIES_COLLECTION = _DB['categorys']
    _USERS_COLLECTION = _DB['users']

    @classmethod
    def close_connection(cls):
        cls._MONGO_CLIENT.close()

    @classmethod
    def is_connection_open(cls) -> bool:
        try:
            cls._MONGO_CLIENT.admin.command('ping')
            return True
        except Exception:
            return False
        
    @classmethod
    def reconnect(cls):
        cls._MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

        cls._DB = cls._MONGO_CLIENT['manager']
        cls._STORES_COLLECTION = cls._DB['stores']
        cls._SPACES_COLLECTION = cls._DB['spaces']
        cls._SHELVES_COLLECTION = cls._DB['shelfs']
        cls._PRODUCTS_COLLECTION = cls._DB['products']
        cls._CATEGORIES_COLLECTION = cls._DB['categorys']
        cls._USERS_COLLECTION = cls._DB['users']

    @classmethod
    def get_many_stores(cls, filter = {}):
        return cls._STORES_COLLECTION.find(filter)

    @classmethod
    def insert_one_store(cls, store):
        cls._STORES_COLLECTION.insert_one(store)

    @classmethod
    def get_many_spaces(cls, filter = {}):
        return cls._SPACES_COLLECTION.find(filter)

    @classmethod
    def insert_many_spaces(cls, spaces):
        cls._STORES_COLLECTION.insert_many(spaces)

    @classmethod
    def update_one_space(cls, filter, new_info):
        cls._STORES_COLLECTION.update_one(filter, new_info)

    @classmethod
    def get_many_shelves(cls, filter = {}):
        return cls._SHELVES_COLLECTION.find(filter)

    @classmethod
    def get_one_shelf(cls, filter = {}):
        return cls._SHELVES_COLLECTION.find_one(filter)

    @classmethod
    def insert_many_shelves(cls, shelves):
        cls._SHELVES_COLLECTION.insert_many(shelves)

    @classmethod
    def get_many_products(cls, filter = {}):
        return cls._PRODUCTS_COLLECTION.find(filter)

    @classmethod
    def get_one_product(cls, filter = {}):
        return cls._PRODUCTS_COLLECTION.find_one(filter)

    @classmethod
    def insert_one_product(cls, product):
        cls._PRODUCTS_COLLECTION.insert_one(product)

    @classmethod
    def update_one_product(cls, filter, new_info):
        cls._PRODUCTS_COLLECTION.update_one(filter, new_info)

    @classmethod
    def delete_one_product(cls, filter):
        cls._PRODUCTS_COLLECTION.delete_one(filter)

    @classmethod
    def get_many_categories(cls, filter = {}):
        return cls._CATEGORIES_COLLECTION.find(filter)

    @classmethod
    def get_one_category(cls, filter = {}):
        return cls._CATEGORIES_COLLECTION.find_one(filter)

    @classmethod
    def insert_one_category(cls, category):
        cls._CATEGORIES_COLLECTION.insert_one(category)

    @classmethod
    def update_one_category(cls, filter, new_info):
        cls._CATEGORIES_COLLECTION.update_one(filter, new_info)

    @classmethod
    def delete_one_category(cls, filter):
        cls._CATEGORIES_COLLECTION.delete_one(filter)

    @classmethod
    def get_one_user(cls, filter = {}):
        return cls._USERS_COLLECTION.find_one(filter)

    @classmethod
    def insert_one_user(cls, user):
        cls._USERS_COLLECTION.insert_one(user)

    @classmethod
    def delete_one_user(cls, filter):
        cls._USERS_COLLECTION.delete_one(filter)

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
                cls.insert_many_spaces(local_shelf['spaces'])
            except (ConnectionFailure, ServerSelectionTimeoutError):
                UserManager.set_user('Guest', 'Offline')
                QMessageBox.warning(None, "The spaces were not created", "There was an issue with the network")
                break

            insert_shelf['spaces'] = cls.get_last_spaces_created(len(local_shelf['spaces']))

            insert_shelves.append(insert_shelf)

        try:
            cls.insert_many_shelves(insert_shelves)
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The shelves were not created", "There was an issue with the network")

    @classmethod
    def get_last_spaces_created(cls, num) -> list:
        spaces = []

        try:
            db_spaces = cls.get_many_spaces().sort([('creation_date', -1)]).limit(num)

            for mongo_space in db_spaces:
                spaces.append(mongo_space['_id'])
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Spaces not found", "There was an issue with the network")

        return spaces

    @classmethod
    def get_last_shelves_created(cls, num) -> list:
        shelves = []

        try: 
            db_shelves = cls.get_many_shelves().sort([('creation_date', -1)]).limit(num)

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
            cls.insert_one_store({ "name": name, "image": image, "storeShelves": id_shelves, "storeFloors": max_floor })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The store was not created", "There was an issue with the network")

    @classmethod
    def get_category_by_name(cls, name) -> str:
        try:
            file = cls.get_one_category({ "name": name })

            return file['_id']
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return name

    @classmethod
    def update_category_space(cls, space_id, category_name):
        if space_id != None:
            category_id = cls.get_category_by_name(category_name)

            try:
                cls.update_one_space({ "mongo_id": space_id }, { "$set": { "category": category_id } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def update_category_name(cls, old_name, new_name):
        try:
            cls.update_one_category({ "name": old_name }, { "$set": { "name": new_name } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def update_category_color(cls, name, color):
        try:
            cls.update_one_category({ "name": name }, { "$set": { "color": color } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def delete_by_name(cls, name):
        try:
            cls.delete_one_category({ "name": name })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The user was not deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the user", f"Write error: {e.details}")

    @classmethod
    def add_category(cls, name, color, can_hold_product):
        try:
            cls.insert_one_category({
                "name": name,
                "color": color,
                "hold": can_hold_product
            })
        except (ConnectionFailure, ServerSelectionTimeoutError):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not created", "There was an issue with the network")

    @classmethod
    def update_category_holds_product(cls, category_name, holds_product):
        category_id = cls.get_category_by_name(category_name)

        try:
            cls.update_one_category({ "_id": category_id }, { "$set": { "hold": holds_product } })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The category was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The category was not updated", f"Operation failed: {e.details}")

    @classmethod
    def get_products(cls) -> list:
        try:
            products = []

            for db_product in cls.get_many_products():
                products.append({ "name": db_product['name'].capitalize(), "price": db_product['price'] })

            return products

        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Products not found", "There was an issue with the network")

            return []
    
    @classmethod
    def add_product(cls, product_name: str, price: float):
        try:
            cls.insert_one_product({
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
                cls.update_one_space({ "mongo_id": space_id }, { "$set": { "amount": amount } })
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def get_product_by_name(cls, name_product: str) -> str | None:
        try:
            file = cls.get_one_product({ "name": name_product.lower() })

            return file['_id']
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Category not found", "There was an issue with the network")

            return None

    @classmethod
    def update_space_product(cls, space_id, new_product):
        if space_id != None:
            try:
                if new_product != '':
                    product_id = cls.get_product_by_name(new_product)

                    if product_id != None:
                        cls.update_one_space({ "mongo_id": space_id }, { "$set": { "product": product_id } })
                    else:
                        QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
                else:
                    cls.update_one_space({ "mongo_id": space_id }, { "$unset": { "product": "" } })

            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
                UserManager.set_user('Guest', 'Offline')
                QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
            except (OperationFailure, WriteError) as e:
                QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def update_product(cls, old_name, new_name: str, new_price: float):
        try:
            product_id = cls.get_product_by_name(old_name)

            if product_id != None:
                cls.update_one_product({ "_id": product_id }, { "$set": { "name": new_name.lower(), "price": new_price } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def update_product_name(cls, old_name, new_name: str):
        try:
            product_id = cls.get_product_by_name(old_name)

            if product_id != None:
                cls.update_one_product({ "_id": product_id }, { "$set": { "name": new_name.lower() } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def update_product_price(cls, old_name, new_price: float):
        try:
            product_id = cls.get_product_by_name(old_name)

            if product_id != None:
                cls.update_one_product({ "_id": product_id }, { "$set": { "price": new_price } })
            else:
                QMessageBox.warning(None, "The product was not found", "Check if the name is correct")
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The space was not updated", "There was an issue with the network")
        except (OperationFailure, WriteError) as e:
            QMessageBox.warning(None, "The space was not updated", f"Operation failed: {e.details}")

    @classmethod
    def del_product(cls, prduct_name: str):
        try:
            cls.delete_one_product({ "name": prduct_name.lower() })
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "The product was not deleted", "There was an issue with the network")
        except WriteError as e:
            QMessageBox.warning(None, "There was an issue deleting the product", f"Write error: {e.details}")
