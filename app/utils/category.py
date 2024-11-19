from app.constants import CATEGORY_NAMES, CATEGORY_COLORS

class Category():
    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def addCategory(name, color):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)

    def delCategory(index):
        CATEGORY_COLORS.pop(index)
        CATEGORY_NAMES.pop(index)

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
