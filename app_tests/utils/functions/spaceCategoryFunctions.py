from app_tests.constants import CATEGORY_NAMES, CATEGORY_COLORS, WINDOW_HEIGHT

from app_tests.utils.category import Category

from app_tests.components.doubleButton import DoubleButton

def createCategoryIn(space, categoryName, parent):
    # Create a button to acces the config of the category
    newDoubleButton = DoubleButton(categoryName, "❌", space.editCategory, space.deleteCategory, parent)
    newDoubleButton.setGeometry(0, 0, 450, 69)

    space.doubleButtons.append(newDoubleButton)

def updateNameCategory(space, color, actualName, newName, shortcut = False):
    if not shortcut:
        # Change the name of the button with the actual category to the new name for the category
        for button in space.category.doubleButtons:
                if button.textButton1() == actualName:
                    button.setTextButton1(newName)
                    break

        # Updates the name in the comboBox
        for i in range(space.categorySelector.count()):
            if space.categorySelector.itemText(i) == actualName:
                space.categorySelector.setItemText(i, newName)

        if space.category.color == color:    
            # Updates the name in the space
            space.category.name = newName
    else:
        for button in space.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)
                break

def deleteCategoryFrom(space, indexButtonPressed, categoryName, shortcut = False):
    if not shortcut:
        items = []

        for index in range(space.categorySelector.count()):
            items.append(space.categorySelector.itemText(index))

        # Removes the category from the comboBox
        for index, item in enumerate(items):
            if item == categoryName:
                space.categorySelector.removeItem(index)

        # Hide the buttons before removing them
        space.category.doubleButtons[indexButtonPressed].hide()
        space.category.doubleButtons.pop(indexButtonPressed)

        if space.category.name == categoryName:
            if indexButtonPressed > 0:
                space.category.name = space.category.doubleButtons[indexButtonPressed - 1].textButton1()
            else:
                space.category.name = space.category.doubleButtons[indexButtonPressed].textButton1()
            
            space.category.color = Category.getColorByName(space.category.name)
    else:
        # Hide the buttons before removing them
        space.doubleButtons[indexButtonPressed].hide()
        space.doubleButtons.pop(indexButtonPressed)

def updateButtonsPosition(space):
    posx = 13
    posy = 24

    for index, _ in enumerate(CATEGORY_NAMES):
        space.doubleButtons[index].setGeometry(posx, posy, 450, 69)

        if posy + 100 >= WINDOW_HEIGHT:
            posx += 400
            posy = 24
        else:
            posy += 50

    if posy + 150 >= WINDOW_HEIGHT:
        posx += 400
        posy = 24

    space.addCategory.move(posx + 25, posy + 13)

    if space.doubleButtons.__len__() >= 37:
        space.addCategory.hide()
    else:
        space.addCategory.show()

def setEmptyCategory(category):
    if CATEGORY_NAMES.__len__() > 0:
        category.name = CATEGORY_NAMES[0]
        category.color = CATEGORY_COLORS[0]

def setUnreachableCategory(category):
    if CATEGORY_NAMES.__len__() > 1:
        category.name = CATEGORY_NAMES[1]
        category.color = CATEGORY_COLORS[1]

def setCategoryByName(category, name):
    category.name = name
    category.color = Category.getColorByName(name)

def getEmptyCategoryName():
    if CATEGORY_NAMES.__len__() > 0:
        return CATEGORY_NAMES[0]

    return None

def getUnreachableCategoryName():
    if CATEGORY_NAMES.__len__() > 1:
        return CATEGORY_NAMES[1]
    
    return None