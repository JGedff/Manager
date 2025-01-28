from constants import PRODUCTS_INFO

class ProductManager():
    @staticmethod
    def add(product_name: str, price: float):
        PRODUCTS_INFO.append([product_name.capitalize(), price])
    
    @staticmethod
    def get(index: int) -> list:
        return PRODUCTS_INFO[index]

    @staticmethod
    def get_by_name(product_name: str) -> list:
        for product in PRODUCTS_INFO:
            if product[0] == product_name.capitalize():
                return product

        return []

    @staticmethod
    def update_product(index: int, new_product_name: str, price: float):
        PRODUCTS_INFO[index][0] = new_product_name.capitalize()
        PRODUCTS_INFO[index][1] = price

    @staticmethod
    def update_product_name(index: int, new_product_name: str):
        PRODUCTS_INFO[index][0] = new_product_name.capitalize()

    @staticmethod
    def update_product_price(index: int, price: float):
        PRODUCTS_INFO[index][1] = price

    @staticmethod
    def get_index_by_name(product_name: str):
        for i, prod in enumerate(PRODUCTS_INFO):
            if prod[0] == product_name.capitalize():
                return i

        return -1

    @staticmethod
    def delete_by_name(product_name: str):
        index = ProductManager.get_index_by_name(product_name)

        if index != -1:
            PRODUCTS_INFO.pop(index)

    @staticmethod
    def count():
        return len(PRODUCTS_INFO)

    @staticmethod
    def get_all_products():
        return PRODUCTS_INFO
