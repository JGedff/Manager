from constants import PRODUCTS_INFO

class Product():
    def getAll():
        return PRODUCTS_INFO
    
    def get(id):
        return PRODUCTS_INFO[id]

    def getByName(name):
        for prod in PRODUCTS_INFO:
            if prod.name == name:
                return prod
    
    def set(id, info):
        PRODUCTS_INFO[id] = info

    def delete(id):
        PRODUCTS_INFO.pop(id)