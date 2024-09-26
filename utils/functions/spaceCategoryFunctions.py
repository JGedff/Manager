from utils.category import Category
from utils.doubleButton import DoubleButton

from constants import CATEGORY_NAMES, CATEGORY_COLORS

def createCategoryIn(space, categoryName, parent):
    newDoubleButton = DoubleButton(25, 50 * CATEGORY_NAMES.__len__() - 25, categoryName, "🗑️", space.category.editCategory, space.category.deleteCategory, parent)

    space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)
    space.category.doubleButtons.append(newDoubleButton)
    space.configCategory.addItem(categoryName)

    if space.category.doubleButtons.__len__() > 3:
        space.category.doubleButtons[0].setDisabledButton2(False)

def deleteCategoryFrom(space, indexButtonPressed, categoryName):
    items = []

    for index in range(space.configCategory.count()):
        items.append(space.configCategory.itemText(index))

    for index, item in enumerate(items):
        if item == categoryName:
            space.configCategory.removeItem(index)

    space.category.doubleButtons[indexButtonPressed].hide()
    
    space.category.doubleButtons.pop(indexButtonPressed)
    space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)

    if space.category.doubleButtons.__len__() == 1:
        space.category.doubleButtons[0].setDisabledButton2(True)

def updateButtonsPosition(space):
    posx = 13
    posy = 13

    for index, _ in enumerate(CATEGORY_NAMES):
        space.category.doubleButtons[index].setGeometry(posx, posy, 450, 50)

        posy += 50

def setEmptyCategory(category):
        category.name = CATEGORY_NAMES[0]
        category.color = CATEGORY_COLORS[0]

def setUnreachableCategory(category):
    category.name = CATEGORY_NAMES[1]
    category.color = CATEGORY_COLORS[1]

def setCategoryByName(category, name):
    category.name = name
    category.color = Category.getColorByName(name)