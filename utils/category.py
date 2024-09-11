from constants import CATEGORY_NAMES, CATEGORY_COLORS

class Category():
    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def addCategory(name, color):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)

    def delCategory(index):
        CATEGORY_NAMES.pop(index)
        CATEGORY_COLORS.pop(index)

    def getIndexByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index

    def getColorByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]

    def getIndexByColor(color):
        for index, cat in enumerate(CATEGORY_COLORS):
            if cat.lower() == color.lower():
                return index

    def getNameByIndex(index):
        return CATEGORY_NAMES[index]
