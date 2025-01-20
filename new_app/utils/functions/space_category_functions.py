from constants import CATEGORY_NAMES, CATEGORY_COLORS, WINDOW_HEIGHT

from utils.category import Category

from components.double_button import DoubleButton

def create_category_in(space, category_name, parent):
    space_category = space

    # Create a button to acces the config of the category
    new_double_buttons = DoubleButton(category_name, "❌", space_category.edit_category_function, space_category.delete_category_function, parent)
    new_double_buttons.setGeometry(0, 0, 450, 69)

    space_category.double_buttons.append(new_double_buttons)

def update_category_name(space, color, actual_name, new_name, shortcut = False):
    space_category = space

    if not shortcut:
        space_category = space.category

        if space.category.color == color:
            # Updates the name in the space
            space.category.name = new_name

        # Updates the name in the comboBox of the space
        for i in range(space.category_selector.count()):
            if space.category_selector.itemText(i) == actual_name:
                space.category_selector.setItemText(i, new_name)

    # Change the name of the button with the actual category to the new name for the category
    for button in space_category.double_buttons:
        if button.get_first_button_text() == actual_name:
            button.set_first_button_text(new_name)
            break

def delete_category_from(space, index_button_pressed, category_name, shortcut = False):
    space_category = space

    if not shortcut:
        space_category = space.category

        # Removes the category from the comboBox
        for index in range(space.category_selector.count()):
            if space.category_selector.itemText(index) == category_name:
                space.category_selector.removeItem(index)

        # If the actual category is the same as the category that is going to be deleted
        if space_category.name == category_name:

            # Change the actual category for another category
            if index_button_pressed > 0:
                space_category.name = space_category.double_buttons[index_button_pressed - 1].get_first_button_text()
            else:
                space_category.name = space_category.double_buttons[index_button_pressed].get_first_button_text()
            
            space_category.color = Category.get_color_by_name(space_category.name)

    # Hide the buttons before removing them
    space_category.double_buttons[index_button_pressed].hide()
    space_category.double_buttons.pop(index_button_pressed)

def update_category_buttons_pos(space):
    posx = 13
    posy = 24

    for index in range(len(CATEGORY_NAMES)):
        space.double_buttons[index].setGeometry(posx, posy, 450, 69)

        if posy + 100 >= WINDOW_HEIGHT:
            posx += 400
            posy = 24
        else:
            posy += 50

    if posy + 150 >= WINDOW_HEIGHT:
        posx += 400
        posy = 24

    space.add_category_button.move(posx + 25, posy + 13)

    if len(space.double_buttons) >= 37:
        space.add_category_button.hide()
    else:
        space.add_category_button.show()

def set_empty_category(category):
    if len(CATEGORY_NAMES) > 0:
        category.name = CATEGORY_NAMES[0]
        category.color = CATEGORY_COLORS[0]

def set_unreachable_category(category):
    category.name = CATEGORY_NAMES[1]
    category.color = CATEGORY_COLORS[1]

def set_category_by_name(category, name):
    category.name = name
    category.color = Category.get_color_by_name(name)

def get_empty_category_name():
    return CATEGORY_NAMES[0]

def get_unreachable_category_name():
    return CATEGORY_NAMES[1]
