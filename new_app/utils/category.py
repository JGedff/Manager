from constants import CATEGORY_NAMES, CATEGORY_COLORS, CATEGORY_HOLDS_PRODUCT

class Category():
    @staticmethod
    def del_all_categories():
        while len(CATEGORY_NAMES) > 0:
            CATEGORY_NAMES.pop()
            CATEGORY_COLORS.pop()
            CATEGORY_HOLDS_PRODUCT.pop()

    def change_category_color(index: int, color: str):
        CATEGORY_COLORS[index] = color

    def change_category_name(index: int, name: str):
        CATEGORY_NAMES[index] = name

    def add_category(name: str, color: str):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)
        CATEGORY_HOLDS_PRODUCT.append(False)

    def del_category(index: int):
        CATEGORY_COLORS.pop(index)
        CATEGORY_NAMES.pop(index)
        CATEGORY_HOLDS_PRODUCT.pop(index)

    def get_index_by_name(name: str):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index
            
        return -1

    def get_color_by_name(name: str) -> str:
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]
        
        return "#000000"

    def get_name_by_index(index: int) -> str:
        return CATEGORY_NAMES[index]
    
    def can_hold_product(name: str) -> bool:
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_HOLDS_PRODUCT[index]
        
        return False

    def change_can_hold_product(category: str, val: bool):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == category.lower():
                CATEGORY_HOLDS_PRODUCT[index] = val
