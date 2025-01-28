from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout

from PyQt5.QtWidgets import QWidget, QMessageBox

from constants import SHELVES_FORMS, STORES, SHELVES

from utils.mongo_db import Mongo
from utils.category import Category
from utils.user_manager import UserManager

from utils.functions.space_category_functions import create_category_in, update_category_buttons_pos, set_empty_category
from utils.functions.shelf_functions import save_shelves_info

from components.shelf import ShelfForm

def get_information(widget: QWidget | None, shortcut_category, main_window):
    store_index = 0
    num_categories = 0
    connection_open = False

    try:
        for category in Mongo.get_many_categories():
            Category.add_category(category['name'], category['color'])
            Category.change_can_hold_product(category['name'], category['hold'])

            create_category_in(shortcut_category, category['name'], widget)
            num_categories += 1

        update_category_buttons_pos(shortcut_category)

    except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
        UserManager.set_user('Guest', 'Offline')

        QMessageBox.warning(None, "Categories not found", "There was an issue with the network")

        Category.add_category('Empty', 'white')
        Category.add_category('Unreachable', 'red')
        Category.add_category('Fill', 'green')
        Category.change_can_hold_product('Fill', True)

        create_category_in(shortcut_category, 'Empty', widget)
        create_category_in(shortcut_category, 'Unreachable', widget)
        create_category_in(shortcut_category, 'Fill', widget)
        update_category_buttons_pos(shortcut_category)

        num_categories = 0

    else:
        connection_open = True

        if num_categories <= 0:
            QMessageBox.warning(None, "There aren't any categories in the database", "The default categories will be created")

            Mongo.add_category('Empty', 'white', False)
            Mongo.add_category('Unreachable', 'red', False)
            Mongo.add_category('Fill', 'green', True)

            Category.add_category('Empty', 'white')
            Category.add_category('Unreachable', 'red')
            Category.add_category('Fill', 'green')
            Category.change_can_hold_product('Fill', True)

            create_category_in(shortcut_category, 'Empty', widget)
            create_category_in(shortcut_category, 'Unreachable', widget)
            create_category_in(shortcut_category, 'Fill', widget)
            update_category_buttons_pos(shortcut_category)

    set_empty_category(shortcut_category)

    if connection_open:
        try:
            for store in Mongo.get_many_stores():
                spacesInfo = []

                for index, shelf_id in enumerate(store['storeShelves']):
                    shelf = Mongo.get_one_shelf({ "_id": shelf_id })
                    mongoSpaces = Mongo.get_many_spaces({"_id": {"$in": shelf['spaces']}})
                    
                    ShelfForm.create(widget, main_window)

                    SHELVES_FORMS[index].input_spaces.set_value(shelf['spaces'].__len__() / store['storeFloors'])
                    SHELVES_FORMS[index].input_shelf_floors.set_value(shelf['floors'])
                    SHELVES_FORMS[index].double_shelf_input.set_value(shelf['double_shelf'])
                    SHELVES_FORMS[index].hide()

                    spacesInfo.append(mongoSpaces)
                
                save_shelves_info(SHELVES_FORMS)
                
                Store.create_store(store['name'], widget, store['image'], main_window)

                STORES[store_index].return_to_store_button.hide()

                for shelfIndex in range(store['storeShelves'].__len__()):
                    for index, mongoSpace in enumerate(spacesInfo[shelfIndex]):
                        SHELVES[store_index][shelfIndex].spaces[index].mongo_id = mongoSpace['mongo_id']

                        if num_categories > 0:
                            category = Mongo.get_one_category({ "_id": mongoSpace['category'] })

                            if category != None:
                                SHELVES[store_index][shelfIndex].spaces[index].category_selector.setCurrentText(category['name'])
                                SHELVES[store_index][shelfIndex].spaces[index].category.name = category['name']
                                SHELVES[store_index][shelfIndex].spaces[index].category.color = category['color']

                                if isinstance(SHELVES[store_index][shelfIndex].spaces[index].product, Product):
                                    SHELVES[store_index][shelfIndex].spaces[index].product.hide()
                
                store_index =+ 1
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
            UserManager.set_user('Guest', 'Offline')
            QMessageBox.warning(None, "Network error", "There was an issue with the network")
