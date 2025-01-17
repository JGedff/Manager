from constants import CATEGORY_NAMES, CATEGORY_COLORS, WINDOW_HEIGHT

from utils.category import Category

from components.double_button import DoubleButton

def create_category_in(space, categoryName, parent, shortcut = False):
    if not shortcut:
        # Create a button to acces the config of the category
        new_double_buttons = DoubleButton(categoryName, "❌", space.category.editCategory, space.category.deleteCategory, parent)
        new_double_buttons.setGeometry(0, 0, 450, 69)

        space.category.double_buttons.append(new_double_buttons)
    else:
        # Create a button to acces the config of the category
        new_double_buttons = DoubleButton(categoryName, "❌", space.editCategory, space.deleteCategory, parent)
        new_double_buttons.setGeometry(0, 0, 450, 69)

        space.double_buttons.append(new_double_buttons)

def updateNameCategory(space, color, actualName, newName, shortcut = False):
    if not shortcut:
        if space.category.color == color:
            # Change the name of the button with the actual category to the new name for the category
            for button in space.category.double_buttons:
                if button.get_first_button_text() == actualName:
                    button.set_first_button_text(newName)
                    break

            # Updates the name in the comboBox
            for i in range(space.categorySelector.count()):
                if space.categorySelector.itemText(i) == actualName:
                    space.categorySelector.setItemText(i, newName)

            # Updates the name in the space
            space.category.name = newName
        else:
            # Change the name of the button with the actual category to the new name for the category
            for button in space.category.double_buttons:
                if button.get_first_button_text() == actualName:
                    button.set_first_button_text(newName)
                    break
            
            # Updates the name in the comboBox
            for i in range(space.categorySelector.count()):
                if space.categorySelector.itemText(i) == actualName:
                    space.categorySelector.setItemText(i, newName)

    else:
        for button in space.double_buttons:
            if button.get_first_button_text() == actualName:
                button.set_first_button_text(newName)
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
        space.category.double_buttons[indexButtonPressed].hide()
        space.category.double_buttons.pop(indexButtonPressed)

        if space.category.name == categoryName:
            if indexButtonPressed > 0:
                space.category.name = space.category.double_buttons[indexButtonPressed - 1].get_first_button_text()
            else:
                space.category.name = space.category.double_buttons[indexButtonPressed].get_first_button_text()
            
            space.category.color = Category.getColorByName(space.category.name)
    else:
        # Hide the buttons before removing them
        space.double_buttons[indexButtonPressed].hide()
        space.double_buttons.pop(indexButtonPressed)

def update_button_pos(space, shortcut = False):
    posx = 13
    posy = 24

    if not shortcut:
        for index, _ in enumerate(CATEGORY_NAMES):
            space.category.double_buttons[index].setGeometry(posx, posy, 450, 69)

            if posy + 100 >= WINDOW_HEIGHT:
                posx += 400
                posy = 24
            else:
                posy += 50

        if posy + 150 >= WINDOW_HEIGHT:
            posx += 400
            posy = 24

        space.category.addCategory.move(posx + 25, posy + 13)

        if space.category.double_buttons.__len__() >= 37:
            space.category.addCategory.hide()
        else:
            space.category.addCategory.show()
    else:
        for index, _ in enumerate(CATEGORY_NAMES):
            space.double_buttons[index].setGeometry(posx, posy, 450, 69)

            if posy + 100 >= WINDOW_HEIGHT:
                posx += 400
                posy = 24
            else:
                posy += 50

        if posy + 150 >= WINDOW_HEIGHT:
            posx += 400
            posy = 24

        space.addCategory.move(posx + 25, posy + 13)

        if space.double_buttons.__len__() >= 37:
            space.addCategory.hide()
        else:
            space.addCategory.show()

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
