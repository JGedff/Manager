from pymongo import MongoClient

class DB:
    _MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")

    _DB = _MONGO_CLIENT['manager']

    _USERS_COLLECTION = _DB['users']
    _STORES_COLLECTION = _DB['stores']
    _SPACES_COLLECTION = _DB['spaces']
    _SHELVES_COLLECTION = _DB['shelfs']
    _PRODUCTS_COLLECTION = _DB['products']
    _CATEGORIES_COLLECTION = _DB['categorys']

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

        cls._USERS_COLLECTION = cls._DB['users']
        cls._STORES_COLLECTION = cls._DB['stores']
        cls._SPACES_COLLECTION = cls._DB['spaces']
        cls._SHELVES_COLLECTION = cls._DB['shelfs']
        cls._PRODUCTS_COLLECTION = cls._DB['products']
        cls._CATEGORIES_COLLECTION = cls._DB['categorys']
    
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