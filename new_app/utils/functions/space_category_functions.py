from constants import CATEGORY_NAMES, CATEGORY_COLORS, WINDOW_HEIGHT

from utils.category import Category

from components.double_button import DoubleButton

def create_category_in(space, category_name, parent):
    space_category = space

    # Create a button to acces the config of the category
    new_double_buttons = DoubleButton(category_name, "❌", space_category.edit_category_function, space_category.delete_category_function, parent)
    new_double_buttons.setGeometry(0, 0, 450, 69)

    space_category.double_buttons.append(new_double_buttons)

def update_category_name(space, color, actualName, newName, shortcut = False):
    space_category = space

    if not shortcut:
        space_category = space.category

        if space.category.color == color:
            # Updates the name in the space
            space.category.name = newName

        # Updates the name in the comboBox of the space
        for i in range(space.categorySelector.count()):
            if space.categorySelector.itemText(i) == actualName:
                space.categorySelector.setItemText(i, newName)

    # Change the name of the button with the actual category to the new name for the category
    for button in space_category.double_buttons:
        if button.get_first_button_text() == actualName:
            button.set_first_button_text(newName)
            break

def delete_category_from(space, indexButtonPressed, categoryName, shortcut = False):
    space_category = space

    if not shortcut:
        space_category = space.category

        # Removes the category from the comboBox
        for index in range(space.categorySelector.count()):
            if space.categorySelector.itemText(index) == categoryName:
                space.categorySelector.removeItem(index)

        # If the actual category is the same as the category that is going to be deleted
        if space_category.name == categoryName:

            # Change the actual category for another category
            if indexButtonPressed > 0:
                space_category.name = space_category.double_buttons[indexButtonPressed - 1].get_first_button_text()
            else:
                space_category.name = space_category.double_buttons[indexButtonPressed].get_first_button_text()
            
            space_category.color = Category.get_color_by_name(space_category.name)

    # Hide the buttons before removing them
    space_category.double_buttons[indexButtonPressed].hide()
    space_category.double_buttons.pop(indexButtonPressed)

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
