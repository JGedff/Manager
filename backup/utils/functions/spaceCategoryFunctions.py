from utils.category import Category
from utils.doubleButton import DoubleButton

from constants import CATEGORY_NAMES, CATEGORY_COLORS

def createCategoryIn(space, categoryName, parent):
    # Create a button to acces the config of the category
    newDoubleButton = DoubleButton(25, 50 * CATEGORY_NAMES.__len__() - 25, categoryName, "🗑️", space.category.editCategory, space.category.deleteCategory, parent)
    space.category.doubleButtons.append(newDoubleButton)

    # Updates the position of the form to create a new category
    space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)

    # Add the new category to the comboBox
    space.categorySelector.addItem(categoryName)

def updateNameCategory(space, color, actualName, newName, index):
    if space.category.color == color:
        # Change the name of the button with the actual category to the new name for the category
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)
                break

        # Updates the name in the comboBox
        space.categorySelector.setItemText(index, newName)

        # Updates the name in the space
        space.category.name = newName
    else:
        # Change the name of the button with the actual category to the new name for the category
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)
                break
        
        # Updates the name in the comboBox
        space.categorySelector.setItemText(index, newName)

def deleteCategoryFrom(space, indexButtonPressed, categoryName):
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

    # Moves the form to add a new category
    space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)

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