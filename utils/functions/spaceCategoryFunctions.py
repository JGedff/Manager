from utils.category import Category
from utils.doubleButton import DoubleButton

from constants import CATEGORY_NAMES, CATEGORY_COLORS

def createCategoryIn(space, categoryName, parent, shortcut = False):
    if not shortcut:
        # Create a button to acces the config of the category
        newDoubleButton = DoubleButton(categoryName, "❌", space.category.editCategory, space.category.deleteCategory, parent)
        newDoubleButton.setGeometry(13, 50 * CATEGORY_NAMES.__len__() - 25, 450, 69)

        space.category.doubleButtons.append(newDoubleButton)

        # Updates the position of the form to create a new category
        space.category.addCategory.move(38, 50 * CATEGORY_NAMES.__len__() + 38)

        # Add the new category to the comboBox
        space.categorySelector.addItem(categoryName)
    else:
        # Create a button to acces the config of the category
        newDoubleButton = DoubleButton(categoryName, "❌", space.editCategory, space.deleteCategory, parent)
        newDoubleButton.setGeometry(13, 50 * CATEGORY_NAMES.__len__() - 25, 450, 69)

        space.doubleButtons.append(newDoubleButton)

        # Updates the position of the form to create a new category
        space.addCategory.move(38, 50 * CATEGORY_NAMES.__len__() + 38)

def updateNameCategory(space, color, actualName, newName, shortcut = False):
    if not shortcut:
        if space.category.color == color:
            # Change the name of the button with the actual category to the new name for the category
            for button in space.category.doubleButtons:
                if button.textButton1() == actualName:
                    button.setTextButton1(newName)
                    break

            # Updates the name in the comboBox
            for i in range(space.categorySelector.count()):
                if space.categorySelector.itemText(i) == actualName:
                    space.categorySelector.setItemText(i, newName)

            # Updates the name in the space
            space.category.name = newName
        else:
            # Change the name of the button with the actual category to the new name for the category
            for button in space.category.doubleButtons:
                if button.textButton1() == actualName:
                    button.setTextButton1(newName)
                    break
            
            # Updates the name in the comboBox
            for i in range(space.categorySelector.count()):
                if space.categorySelector.itemText(i) == actualName:
                    space.categorySelector.setItemText(i, newName)
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
                space.category.name = space.category.doubleButtons[indexButtonPressed - 1].button1.text()
            else:
                space.category.name = space.category.doubleButtons[indexButtonPressed].button1.text()
            
            space.category.color = Category.getColorByName(space.category.name)
            #space.categorySelector.setCurrentText(space.category.name)

        # Moves the form to add a new category
        space.category.addCategory.move(38, 50 * CATEGORY_NAMES.__len__() + 38)
    else:
        # Hide the buttons before removing them
        space.doubleButtons[indexButtonPressed].hide()
        space.doubleButtons.pop(indexButtonPressed)

        # Moves the form to add a new category
        space.addCategory.move(38, 50 * CATEGORY_NAMES.__len__() + 38)

def updateButtonsPosition(space, shortcut = False):
    posx = 13
    posy = 24

    if not shortcut:
        for index, _ in enumerate(CATEGORY_NAMES):
            space.category.doubleButtons[index].setGeometry(posx, posy, 450, 69)

            posy += 50
    else:
        for index, _ in enumerate(CATEGORY_NAMES):
            space.doubleButtons[index].setGeometry(posx, posy, 450, 69)

            posy += 50

def setEmptyCategory(category):
    if CATEGORY_NAMES.__len__() > 0:
        category.name = CATEGORY_NAMES[0]
        category.color = CATEGORY_COLORS[0]

def setUnreachableCategory(category):
    category.name = CATEGORY_NAMES[1]
    category.color = CATEGORY_COLORS[1]

def setCategoryByName(category, name):
    category.name = name
    category.color = Category.getColorByName(name)

def getEmptyCategoryName():
    return CATEGORY_NAMES[0]

def getUnreachableCategoryName():
    return CATEGORY_NAMES[1]