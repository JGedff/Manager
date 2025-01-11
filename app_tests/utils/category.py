from constants import CATEGORY_NAMES, CATEGORY_COLORS, CATEGORY_HOLDS_PRODUCT

class Category():
    @staticmethod
    def delAll():
        while CATEGORY_NAMES.__len__() > 0:
            CATEGORY_NAMES.pop()
            CATEGORY_COLORS.pop()
            CATEGORY_HOLDS_PRODUCT.pop()

    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def addCategory(name, color):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)
        CATEGORY_HOLDS_PRODUCT.append(False)

    def delCategory(index):
        CATEGORY_COLORS.pop(index)
        CATEGORY_NAMES.pop(index)
        CATEGORY_HOLDS_PRODUCT.pop(index)

    def getIndexByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index
            
        return -1

    def getColorByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]
        
        return "#000000"

    def getNameByIndex(index):
        return CATEGORY_NAMES[index]
    
    def categoryCanHoldProduct(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_HOLDS_PRODUCT[index]
        
        return False

    def changeCategoryCanHoldProduct(name, val):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                CATEGORY_HOLDS_PRODUCT[index] = val