from constants import CATEGORY_NAMES, CATEGORY_COLORS, PRODUCT_CATEGORY

class Category():
    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def addCategory(name, color, product = False):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)

        if product:
            PRODUCT_CATEGORY.append(name)

    def delCategory(index):
        delIndex = -1

        for newIndex, categoryName in enumerate(PRODUCT_CATEGORY):
            if categoryName == CATEGORY_NAMES[index]:
                delIndex = newIndex
                break
        
        # If category exists, remove it
        if delIndex != -1:
            PRODUCT_CATEGORY.pop(delIndex)

        CATEGORY_COLORS.pop(index)
        CATEGORY_NAMES.pop(index)

    def getIndexByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index

    def getColorByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]

    def getNameByIndex(index):
        return CATEGORY_NAMES[index]
    
    def isProductCategory(name):
        for categoryName in PRODUCT_CATEGORY:
            if categoryName == name:
                return True
        
        return False
