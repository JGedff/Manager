import os
import sys
import shutil
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QMessageBox, QFileDialog, QColorDialog
from PyQt5.QtCore import Qt

from styles.style_sheets import INPUT_TEXT, DEFAULT_BUTTON, COMBO_BOX, BLUE_BUTTON, EDIT_BUTTON, IMPORTANT_ACTION_BUTTON, BACKGROUND_GREY, OFF_BUTTON
from styles.fonts import FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR, FONT_SMALL_BOLD_TEXT
from styles.color_functions import get_style_sheet

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS, STORES, DEFAULT_IMAGE, SHELVES, CATEGORY_NAMES

from utils.functions.global_functions import get_max_floor
from utils.functions.shelf_functions import save_shelves_info, update_shelves_pos
from utils.functions.space_category_functions import set_unreachable_category, set_category_by_name, get_unreachable_category_name, get_empty_category_name, update_category_buttons_pos, set_empty_category, update_category_name, create_category_in, delete_category_from

from utils.db import DB
from utils.mongo_db import Mongo
from utils.user_manager import UserManager

from utils.language import Language
from utils.category import Category

from components.shelf import ShelfForm
from components.product import Product
from components.log_in import LogInWindow
from components.input_bool import InputBool
from components.image_button import ImageButton
from components.double_button import DoubleButton
from components.language_changer import LanguageChanger

app = QApplication(sys.argv)

class CategorySpace(QLabel):
    def __init__(self, parent_space, parent = None, shortcut = False):
        super().__init__(parent)

        self.init_variables(parent_space, parent, shortcut)
        self.init_ui(parent)
        self.init_events()

        set_empty_category(self)

    def init_variables(self, parent_space, parent, shortcut):
        self.name = ''
        self.color = ''
        self._updated_color = ''
        self._shortcut = shortcut
        self._main_parent = parent
        self._name_new_category = ''
        self.categories_buttons = []
        self._color_new_category = ''
        self._creating_category = False
        self._name_modified_categoy = ''
        self._parent_space = parent_space
        self._color_modified_category = ''

    def init_ui(self, parent):
        ## INITIALIZE OBJECTS ##
        # Labels
        self.label_input_edit_category_color = QLabel(Language.get("category_color"), parent)
        self.label_input_edit_category_color.setGeometry(50, 110, 175, 25)
        self.label_input_edit_category_color.hide()

        self.label_input_edit_category_name = QLabel(Language.get("category_name"), parent)
        self.label_input_edit_category_name.setGeometry(50, 60, 175, 25)
        self.label_input_edit_category_name.hide()

        # Buttons
        self.edit_category_color_selector = QPushButton(Language.get("select_color"), parent)
        self.edit_category_color_selector.setGeometry(250, 100, 138, 39)
        self.edit_category_color_selector.hide()

        self.stop_editting_category = QPushButton(Language.get("go_back"), parent)
        self.stop_editting_category.setGeometry(1260, 10, 140, 50)
        self.stop_editting_category.hide()

        self.update_category_button = QPushButton(Language.get("save"), parent)
        self.update_category_button.setGeometry(250, 150, 125, 39)
        self.update_category_button.hide()

        posx = 25
        posy = 25

        for category in CATEGORY_NAMES:
            new_double_button = DoubleButton(category.capitalize(), "❌", self.edit_category_function, self.delete_category_function, parent)
            new_double_button.setGeometry(posx - 12, posy - 12, 450, 69)

            posy += 69
            self.categories_buttons.append(new_double_button)

        self.new_category_color_selector = QPushButton(Language.get("select_color"), parent)
        self.new_category_color_selector.setGeometry(posx + 238, posy - 175, 138, 39)
        self.new_category_color_selector.hide()

        self.cancel_add_category_button = QPushButton(Language.get("cancel"), parent)
        self.cancel_add_category_button.setGeometry(posx + 13, posy, 100, 25)
        self.cancel_add_category_button.hide()

        self.add_category_button = QPushButton(Language.get("add_category"), parent)
        self.add_category_button.setGeometry(posx + 13, posy + 13, 200, 25)
        self.add_category_button.hide()

        self.create_category_button = QPushButton(Language.get("create"), parent)
        self.create_category_button.setGeometry(posx + 438, posy, 100, 25)
        self.create_category_button.setDisabled(True)
        self.create_category_button.hide()

        # Inputs
        self.input_edit_category_name = QLineEdit(parent)
        self.input_edit_category_name.setGeometry(250, 50, 250, 39)
        self.input_edit_category_name.hide()

        self.input_new_category_name = QLineEdit(parent)
        self.input_new_category_name.setGeometry(posx + 13, posy - 100, 250, 39)
        self.input_new_category_name.setPlaceholderText(Language.get("name"))
        self.input_new_category_name.hide()

        ## STYLES ##
        # Labels
        self.label_input_edit_category_name.setAlignment(Qt.AlignRight)
        self.label_input_edit_category_name.setFont(FONT_SMALL_TEXT)

        self.label_input_edit_category_color.setAlignment(Qt.AlignRight)
        self.label_input_edit_category_color.setFont(FONT_SMALL_TEXT)

        # Buttons
        self.add_category_button.setFont(FONT_SMALL_TEXT)
        self.add_category_button.setStyleSheet(BLUE_BUTTON)

        self.stop_editting_category.setFont(FONT_SMALL_TEXT)
        self.stop_editting_category.setStyleSheet(DEFAULT_BUTTON)

        self.create_category_button.setFont(FONT_SMALL_TEXT)
        self.create_category_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)

        self.cancel_add_category_button.setFont(FONT_SMALL_TEXT)
        self.cancel_add_category_button.setStyleSheet(OFF_BUTTON)

        self.update_category_button.setFont(FONT_SMALL_BOLD_TEXT)
        self.update_category_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)

        self.edit_category_color_selector.setFont(FONT_SMALL_TEXT)
        self.edit_category_color_selector.setStyleSheet(get_style_sheet("#FFFFFF"))

        self.new_category_color_selector.setFont(FONT_SMALL_TEXT)
        self.new_category_color_selector.setStyleSheet(get_style_sheet("#FFFFFF"))

        # Inputs
        self.input_edit_category_name.setFont(FONT_SMALL_TEXT)
        self.input_edit_category_name.setStyleSheet(INPUT_TEXT)

        self.input_new_category_name.setFont(FONT_SMALL_TEXT)
        self.input_new_category_name.setStyleSheet(INPUT_TEXT)

    def edit_category_function(self):
        self._updated_color = ''

        self.hide_ui()

        self.add_category_button.hide()
        self.stop_editting_category.show()

        self.cancel_add_category()

        # I don't understand why, but this works to get the text of the category pressed
        self._name_modified_categoy = self.categories_buttons[0].get_first_button_sender_text().strip()

        color = Category.get_color_by_name(self._name_modified_categoy)
        self._color_modified_category = color.stirp()

        self.edit_category_color_selector.setStyleSheet(get_style_sheet(color))

        self.update_category_button.show()
        self.input_edit_category_name.show()
        self.edit_category_color_selector.show()
        self.label_input_edit_category_name.show()
        self.label_input_edit_category_color.show()

        self.input_edit_category_name.setPlaceholderText(self._name_modified_categoy)

        self.update_category_button.raise_()
        self.input_edit_category_name.raise_()
        self.edit_category_color_selector.raise_()

        if self._shortcut:
            window.hide_all_buttons()
        else:
            Store.hide_all_stores()

    def hide_ui(self):
        for category_button in self.categories_buttons:
            category_button.hide()

        self.add_category_button.hide()

        if self._shortcut:
            self.cancel_add_category()
            window.reopen_home_button.show()

    def cancel_add_category(self):
        self._creating_category = False

        self.new_category_color_selector.hide()
        self.cancel_add_category_button.hide()
        self.input_new_category_name.hide()
        self.create_category_button.hide()

        self._name_new_category = ""
        self._color_new_category = ""

        self.create_category_button.setDisabled(True)
        self.add_category_button.setDisabled(self._creating_category)

        for category_button in self.categories_buttons:
            category_button.set_second_button_disabled(self._creating_category)

        self.input_new_category_name.setText("")
        self.new_category_color_selector.setStyleSheet(get_style_sheet("#FFFFFF"))

        if self._creating_category:
            self.add_category_button.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 100)
            self.create_category_button.move(self.create_category_button.pos().x(), self.create_category_button.pos().y() - 100)
            self.input_new_category_name.move(self.input_new_category_name.pos().x(), self.input_new_category_name.pos().y() - 100)
            self.cancel_add_category_button.move(self.cancel_add_category_button.pos().x(), self.cancel_add_category_button.pos().y() - 100)
            self.new_category_color_selector.move(self.new_category_color_selector.pos().x(), self.new_category_color_selector.pos().y() - 100)

    def delete_category_function(self):
        button_pressed = 0

        # This time, like we want the index, something that is not inside the button, I made this to know which category is going to be deleted
        for index, sender_button in enumerate(self.categories_buttons):
            if sender_button.get_second_button() == self.sender():
                button_pressed = index

        category_name = Category.get_name_by_index(button_pressed)

        Category.del_category(button_pressed)

        if UserManager.get_role() != 'Offline':
            Mongo.delete_by_name(category_name)

        delete_category_from(window.shortcut_category, button_pressed, category_name, True)
        update_category_buttons_pos(window.shortcut_category)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if len(space.category.categories_buttons) > len(CATEGORY_NAMES):
                        oldName = space.category.name

                        delete_category_from(space, button_pressed, category_name)
                        update_category_buttons_pos(space.category)

                        if category_name == oldName and UserManager.get_role() != 'Offline':
                            Mongo.update_category_space(space.mongo_id, space.category.name)

        if len(self.categories_buttons) <= 1:
            self.categories_buttons[0].set_second_button_disabled(True)

    def init_events(self):
        self.update_category_button.clicked.connect(self.save_info)
        self.create_category_button.clicked.connect(self.create_category)
        self.add_category_button.clicked.connect(self.show_add_category_ui)
        self.stop_editting_category.clicked.connect(self.stop_edit_category)
        self.new_category_color_selector.clicked.connect(self.select_new_color)
        self.cancel_add_category_button.clicked.connect(self.cancel_add_category)
        self.edit_category_color_selector.clicked.connect(self.select_updated_color)
        self.input_new_category_name.textChanged.connect(self.update_new_category_name)

    def save_info(self):
        updated_name = self.input_edit_category_name.text().capitalize().strip()

        if updated_name != "":
            self.update_categories_name(updated_name)

            if UserManager.get_role() != 'Offline':
                Mongo.update_category_name(self._name_modified_categoy, updated_name)

            self._name_modified_categoy = updated_name

        if self._updated_color != "":
            self.update_categories_color(self._name_modified_categoy)

            if UserManager.get_role() != 'Offline':
                Mongo.update_category_color(self._name_modified_categoy, self._updated_color)

    def update_categories_name(self, updated_name: str):
        index = Category.get_index_by_name(self._name_modified_categoy)
        Category.change_category_name(index, updated_name)

        update_category_name(window.shortcut_category, self._color_modified_category, self._name_modified_categoy, updated_name, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    update_category_name(space, self._color_modified_category, self._name_modified_categoy, updated_name)

    def update_categories_color(self, category_name: str):
        index = Category.get_index_by_name(category_name)
        Category.change_category_color(index, self._updated_color)

        if window.shortcut_category.name == category_name:
            window.shortcut_category.color = self._updated_color

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.name == category_name:
                        space.category.color = self._updated_color

    def create_category(self):
        Category.add_category(self._name_new_category.capitalize(), self._color_new_category)

        if UserManager.get_role() != 'Offline':
            Mongo.add_category(self._name_new_category.capitalize(), self._color_new_category, False)

        create_category_in(window.shortcut_category, self._name_new_category.capitalize(), self._main_parent)
        update_category_buttons_pos(window.shortcut_category)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    create_category_in(space.category, self._name_new_category.capitalize(), self._main_parent)
                    update_category_buttons_pos(space.category)

        self.show_ui()
        self.cancel_add_category()
        self.update_add_category_buttons_pos()

    def show_ui(self):
        for category_button in self.categories_buttons:
            category_button.show()
            category_button.raise_()

        if len(self.categories_buttons) < 37:
            self.add_category_button.show()
            self.add_category_button.raise_()
        else:
            self.add_category_button.hide()

    def update_add_category_buttons_pos(self):
        posx = self.add_category_button.pos().x()
        posy = self.add_category_button.pos().y()

        if posy + 100 >= WINDOW_HEIGHT:
            posx += 450
            posy = 24
        else:
            posy += 100

        self.add_category_button.move(posx, posy)
        self.input_new_category_name.move(posx, posy - 50)
        self.cancel_add_category_button.move(posx, posy + 50)
        self.create_category_button.move(posx + 100, posy + 50)
        self.new_category_color_selector.move(posx + 100, posy - 50)

    def show_add_category_ui(self):
        self._creating_category = True

        self.add_category_button.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() + 100)
        self.input_new_category_name.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 100)
        self.cancel_add_category_button.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 42)
        self.create_category_button.move(self.add_category_button.pos().x() + 275, self.add_category_button.pos().y() - 42)
        self.new_category_color_selector.move(self.add_category_button.pos().x() + 275, self.add_category_button.pos().y() - 100)

        self.add_category_button.setDisabled(self._creating_category)

        self.new_category_color_selector.show()
        self.cancel_add_category_button.show()
        self.input_new_category_name.show()
        self.create_category_button.show()

        self.create_category_button.raise_()
        self.input_new_category_name.raise_()
        self.cancel_add_category_button.raise_()
        self.new_category_color_selector.raise_()

        for button in self.categories_buttons:
            button.set_second_button_disabled(self._creating_category)

    def stop_edit_category(self):
        self.input_edit_category_name.setText("")

        self.show_ui()

        self.stop_editting_category.hide()
        self.update_category_button.hide()
        self.input_edit_category_name.hide()
        self.edit_category_color_selector.hide()
        self.label_input_edit_category_name.hide()
        self.label_input_edit_category_color.hide()

        if self._shortcut:
            window.hide_main_buttons()
        else:
            self._parent_space.return_to_space_config.show()

    def select_new_color(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.new_category_color_selector.setStyleSheet(get_style_sheet(color.name()))
            self._color_new_category = color.name().strip()
        
        if self._color_new_category != "" and self._name_new_category != "":
            self.create_category_button.setDisabled(False)

    def select_updated_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.edit_category_color_selector.setStyleSheet(get_style_sheet(color.name()))
            self._updated_color = color.name()

    def update_new_category_name(self):
        self._name_new_category = self.input_new_category_name.text().strip()

        if self._color_new_category != "" and self._name_new_category != "":
            self.create_category_button.setDisabled(False)

class Space(QLabel):
    @staticmethod
    def create_mongo_spaces(store_name: str, store_floors: int, form, id_empty_category: str, id_unreachable_category: str) -> list:
        spaces = []
        mongo_id = 0

        for floor in range(store_floors):
            for _ in range(form.get_num_spaces()):
                id_category = id_unreachable_category if form.get_num_floors() - 1 < floor else id_empty_category 

                spaces.append({
                    "category": id_category,
                    "mongo_id": store_name + "_" + str(mongo_id),
                    "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                })

                mongo_id += 1

        return spaces


    def __init__(self, pos_x: int, pos_y: int, actual_floor: int, shelf_floors: int, store_i: int, shelf_i: int, space_i: int, parent = None, long = False):
        super().__init__(parent)

        self.setGeometry(pos_x, pos_y, 75, 75)

        self.init_variables(actual_floor, shelf_floors, store_i, shelf_i, parent, long)
        self.init_ui(space_i, parent)
        self.init_events()

    def init_variables(self, actual_floor: int, shelf_floors: int, store_i: int, shelf_i: int, parent, long: bool):
        self._long = long
        self.mongo_id = None
        self._store_i = store_i
        self._actual_floor = actual_floor
        self.shelf_i = shelf_i
        self.category = CategorySpace(self, parent)
        update_category_buttons_pos(self.category)

        if actual_floor > shelf_floors:
            set_unreachable_category(self.category)

    def init_ui(self, space_i: int, parent):
        ## INITIALIZE OBJECTS ##
        # Labels
        self.label_category_selected = QLabel(Language.get("category"), parent)
        self.label_category_selected.setGeometry(152, 75, 100, 25)

        self.shelf_number = QLabel(Language.get("shelf") + str(self.shelf_i + 1), parent)
        self.shelf_number.setGeometry(int(WINDOW_WIDTH / 2) - int(125 / 2), 25, 125, 25)

        self.label_can_hold_product = QLabel(Language.get("category_hold_product"), parent)
        self.label_can_hold_product.setGeometry(152, 124, 260, 25)

        # Buttons
        num_space = space_i + 1
        self.space_number = QPushButton(str(num_space), parent)
        self.space_number.setGeometry(26, 75, 76, 76)

        outside_num_space = str(num_space) if num_space % 5 == 0 else ""
        self.box = QPushButton(outside_num_space, parent)
        self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 151)

        self.return_to_space_config = QPushButton(Language.get("go_back"), parent)
        self.return_to_space_config.setGeometry(1260, 10, 140, 50)

        self.edit_categories_button = QPushButton("⚙️", parent)
        self.edit_categories_button.setGeometry(0, 0, 0, 0)

        if UserManager.get_role() == 'Offline' or UserManager.get_role() == 'Manager':
            self.edit_categories_button.setGeometry(390, 71, 35, 35)
        else:
            self.category_can_hold_product.set_true_button_disabled(True)
            self.category_can_hold_product.set_false_button_disabled(True)

        # Inputs
        self.category_can_hold_product = InputBool(Language.get('yes'), Language.get('no'), parent, self.change_category_can_hold_product, self.change_category_can_not_hold_product)
        self.category_can_hold_product.setGeometry(425, 117, 175, 35)

        # Other
        self.category_selector = QComboBox(parent)
        self.category_selector.setGeometry(250, 74, 125, 30)
        self.category_selector.addItem(self.category.name)
        
        for category_name in CATEGORY_NAMES:
            if category_name != self.category.name:
                self.category_selector.addItem(category_name.capitalize())

        ## STYLES ##
        # Labels
        self.shelf_number.setFont(FONT_TEXT)
        self.label_can_hold_product.setFont(FONT_SMALL_TEXT)
        self.label_category_selected.setFont(FONT_SMALL_TEXT)

        # Buttons
        self.box.setFont(FONT_SMALLEST_CHAR)
        
        self.space_number.setFont(FONT_SMALLEST_CHAR)
        
        self.edit_categories_button.setFont(FONT_SMALL_TEXT)
        self.edit_categories_button.setStyleSheet(EDIT_BUTTON)
        
        self.return_to_space_config.setFont(FONT_SMALL_TEXT)
        self.return_to_space_config.setStyleSheet(DEFAULT_BUTTON)

        if self._long:
            self.box.setFixedHeight(151)
            self.space_number.setFixedHeight(151)
        else:
            self.box.setFixedHeight(76)
            self.space_number.setFixedHeight(76)

        # Other
        self.category_selector.setFont(FONT_SMALL_TEXT)
        self.category_selector.setStyleSheet(COMBO_BOX)

        ## SET VALUES ##
        if Category.can_hold_product(self.category.name):
            self.category_can_hold_product.set_value(True)

        self.update_space_boxes_style()

    def change_category_can_hold_product(self):
        Category.change_can_hold_product(self.category_selector.currentText(), True)

        if not hasattr(self, "product"):
            self.product = Product(153, 165, self, self.parent())
            self.product.show()

            Mongo.update_category_holds_product(self.category_selector.currentText(), True)
            Mongo.update_space_product(self.mongo_id, self.product.select_product.currentText())
            Mongo.update_space_amount(self.mongo_id, 1)
        else:
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.show_hide_create()
    
    def change_category_can_not_hold_product(self):
        Category.change_can_hold_product(self.category_selector.currentText(), False)

        if hasattr(self, "product"):
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.show_hide_create()

            self.product.hide()

            del self.product

            Mongo.update_category_holds_product(self.category_selector.currentText(), False)
            Mongo.update_space_product(self.mongo_id, "")
            Mongo.update_space_amount(self.mongo_id, 0)

    def update_space_boxes_style(self):
        self.box.setStyleSheet(get_style_sheet(self.category.color))
        self.space_number.setStyleSheet(get_style_sheet(self.category.color))

    def init_events(self):
        self.box.clicked.connect(self.show_space_config)
        self.category_selector.currentTextChanged.connect(self.change_category)
        self.edit_categories_button.clicked.connect(self.open_categories_config)
        self.return_to_space_config.clicked.connect(self.stop_editting_categories)

    def show_space_config(self):
        window.hide_all_buttons()

        Store.hide_all_stores()
        Store.open_config_space(STORES[self._store_i])

        self.box.hide()

        self.space_number.show()
        self.shelf_number.show()
        self.category_selector.show()
        self.edit_categories_button.show()
        self.label_can_hold_product.show()
        self.label_category_selected.show()
        self.category_can_hold_product.show()

        if hasattr(self, "product"):
            self.product.show()

        window.resize_scroll_height()

    def change_category(self, category_name: str):
        set_category_by_name(self.category, category_name)

        self.update_space_boxes_style()

        if Category.can_hold_product(category_name):
            self.category_can_hold_product.set_value(True)

            if not hasattr(self, "product"):
                self.product = Product(153, 165, self, self.parent())
                self.product.show()

                Mongo.update_space_product(self.mongo_id, self.product.select_product.currentText())
                Mongo.update_space_amount(self.mongo_id, 1)

        else:
            self.category_can_hold_product.set_value(False)

            if hasattr(self, "product"):
                self.product.hide()

                del self.product

        if UserManager.get_role() != 'Offline':
            Mongo.update_category_space(self.mongo_id, category_name)

    def open_categories_config(self):
        if hasattr(self, "product"):
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.show_hide_create()

        Store.open_config_category(STORES[self._store_i])

        window.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

        self.space_number.hide()
        self.shelf_number.hide()
        self.category_selector.hide()
        self.edit_categories_button.hide()
        self.label_can_hold_product.hide()
        self.label_category_selected.hide()
        self.category_can_hold_product.hide()

        if hasattr(self, "product"):
            self.product.hide()

        self.return_to_space_config.show()

        self.category.show_ui()

    def stop_editting_categories(self):
        self.update_space_boxes_style()

        self.category.cancel_add_category()

        Shelf.hide_all_spaces(SHELVES)

        Store.show_return_to_store_button(STORES[self._store_i])

        self.return_to_space_config.hide()

        self.space_number.show()
        self.shelf_number.show()
        self.category_selector.show()
        self.edit_categories_button.show()
        self.label_can_hold_product.show()
        self.label_category_selected.show()
        self.category_can_hold_product.show()

        if hasattr(self, "product"):
            self.product.show()

    def show_floor(self, floor_num: int):
        if floor_num != self._actual_floor:
            self.hide_space()
        else:
            self.show_space()

    def hide_space(self):
        self.box.hide()
        self.space_number.hide()
        self.shelf_number.hide()
        self.category_selector.hide()
        self.edit_categories_button.hide()
        self.return_to_space_config.hide()
        self.label_can_hold_product.hide()
        self.label_category_selected.hide()
        self.category_can_hold_product.hide()

        if hasattr(self, "product"):
            self.product.hide()

        self.category.hide_ui()

    def show_space(self):
        self.update_space_boxes_style()

        self.space_number.hide()
        self.shelf_number.hide()
        self.category_selector.hide()
        self.edit_categories_button.hide()
        self.return_to_space_config.hide()
        self.label_can_hold_product.hide()
        self.label_category_selected.hide()
        self.category_can_hold_product.hide()

        self.box.show()

        if hasattr(self, "product"):
            if self.product.creating_product:
                self.product.show_hide_create()

            self.product.hide()

        self.box.raise_()

class Shelf():
    @staticmethod
    def create_mongo_shelves(store_name: str, array_forms, id_empty_category: str, id_unreachable_category: str) -> list:
        shelves = []
        store_floors = get_max_floor(array_forms)

        for form in array_forms:
            new_spaces = Space.create_mongo_spaces(store_name, store_floors, form, id_empty_category, id_unreachable_category)

            shelves.append({
                "floors": form.get_num_floors(),
                "spaces": new_spaces,
                "double_shelf": form.is_double_shelf(),
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            })

        return shelves

    @staticmethod
    def hide_all_spaces(array_stores):
        for stores in array_stores:
            for shelf in stores:
                shelf.label_shelf_number.hide()

                for space in shelf.spaces:
                    space.hide_space()
    
    @staticmethod
    def change_floor(array_shelves, number: int):
        for shelf in array_shelves:
            shelf.label_shelf_number.show()

            for space in shelf.spaces:
                space.show_floor(number)
    
    @staticmethod
    def get_max_amount_spaces_in_shelf_from_store(array_shelves):
        maximum = 1

        for shelf in array_shelves:
            num_spaces = len(shelf.spaces)

            if shelf.double_shelf:
                num_spaces = int(num_spaces / 2)

            if num_spaces > maximum:
                maximum = num_spaces

        return maximum

    @staticmethod
    def generate_spaces(pos_x: int, pos_y: int, store_floors: int, double_shelf: bool, amount_spaces: int, shelf_floors: int, store_i: int, shelf_num: int, parent):
        spaces = []

        pos_y += 35

        for floor_i in range(store_floors):
            if double_shelf:
                space_i = 0
                long_spaces = amount_spaces % 2
                side_spaces = (amount_spaces / 2).__trunc__()

                for index_pos in range(side_spaces):
                    spaces.append(Space(pos_x + (75 * index_pos), pos_y, floor_i + 1, shelf_floors, store_i, shelf_num - 1, space_i, parent))

                    space_i += 1

                for index_pos in range(side_spaces):
                    spaces.append(Space(pos_x + (75 * index_pos), pos_y + 75, floor_i + 1, shelf_floors, store_i, shelf_num - 1, space_i, parent))

                    space_i += 1

                if long_spaces > 0:
                    spaces.append(Space(pos_x + (75 * side_spaces), pos_y, floor_i + 1, shelf_floors, store_i, shelf_num - 1, space_i, parent, True))

            else:
                for index_pos in range(amount_spaces):
                    spaces.append(Space(pos_x + (75 * index_pos), pos_y, floor_i + 1, shelf_floors, store_i, shelf_num - 1, index_pos, parent))

        return spaces

    def __init__(self, pos_x: int, pos_y: int, shelf_floors: int, amount_spaces: int, double_shelf: bool, store_floors: int, shelf_num = 1, store_i = 1, parent = None):
        self.init_variables(shelf_floors, double_shelf, shelf_num)
        self.init_ui(pos_x, pos_y, amount_spaces, store_floors, store_i, parent)
        self.init_events()
    
    def init_variables(self, shelf_floors: int, double_shelf: bool, shelf_num: int):
        self.spaces = []
        self.shelf_num = shelf_num
        self._amount_floors = shelf_floors
        self.double_shelf = double_shelf

    def init_ui(self, pos_x: int, pos_y: int, amount_spaces: int, store_floors: int, store_i: int, parent):
        ## INITIALIZE OBJECTS ##
        # Labels
        self.label_shelf_number = QLabel(Language.get("shelf") + str(self.shelf_num) + ":", parent)
        self.label_shelf_number.setGeometry(int(WINDOW_WIDTH / 2 - 125 / 2), pos_y, 125, 25)
        self.label_shelf_number.hide()

        ## STYLE ##
        # Labels
        self.label_shelf_number.setFont(FONT_TEXT)

        ## SET VALUES ##
        self.spaces = self.generate_spaces(pos_x, pos_y, store_floors, self.double_shelf, amount_spaces, self._amount_floors, store_i, self.shelf_num, parent)

    def init_events(self):
        window.scroll.horizontalScrollBar().valueChanged.connect(self.update_ui_horizontal_pos)

    def update_ui_horizontal_pos(self, value):
        self.label_shelf_number.move(value + int(WINDOW_WIDTH / 2 - self.label_shelf_number.width() / 2), self.label_shelf_number.pos().y())

class Store():
    @staticmethod
    def create_mongo_store(store_name: str, image = DEFAULT_IMAGE):
        # Save the uploaded image locally
        image_path = image

        if image != DEFAULT_IMAGE:
            save_dir = "img"
            os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Create path of the copy
            file_name = os.path.basename(image)
            save_path = os.path.join(save_dir, file_name)
            image_path = save_path

            shutil.copy(image, save_path) # Copy image to the new path


        empty_category_name = get_empty_category_name()
        unreachable_category_name = get_unreachable_category_name()
        id_empty_category = Mongo.get_category_by_name(empty_category_name)
        id_unreachable_category = Mongo.get_category_by_name(unreachable_category_name)

        new_shelves = Shelf.create_mongo_shelves(store_name, SHELVES_FORMS, id_empty_category, id_unreachable_category)
            
        Mongo.add_store(new_shelves, store_name, image_path)

    @staticmethod
    def create_store(store_name: str, parent, image = DEFAULT_IMAGE):
        posx = 25
        posy = 25

        for _ in range(len(STORES)):
            posx += 170

            if posx + 170 >= WINDOW_WIDTH:
                posx = 25
                posy += 170

        STORES.append(Store(posx, posy, store_name, image, parent))

        SHELVES_FORMS.clear()

    @staticmethod
    def hide_all_store_icons(array_stores):
        for store in array_stores:
            store.hide_icon()

    @staticmethod
    def show_all_store_icons(array_stores):
        for store in array_stores:
            store.show_icon()
            store.raise_icon()

    @staticmethod
    def hide_all_stores(array_stores):
        for store in array_stores:
            store.hide_store()

    @staticmethod
    def open_config_space(store):
        store.floor_selector.hide()
        store.return_to_store_button.show()

    @staticmethod
    def open_config_category(store):
        store.return_to_store_button.hide()

    @staticmethod
    def show_return_to_store_button(store):
        store.return_to_store_button.show()

    def __init__(self, pos_x: int, pos_y: int, store_name: str, store_icon: str, parent):
        self.init_variables(parent)
        self.init_ui(pos_x, pos_y, store_name, store_icon, parent)
        self.init_events()

        update_shelves_pos(SHELVES_FORMS)
    
    def init_variables(self, parent):
        self.store_index = len(STORES)
        self.amount_floors = get_max_floor(SHELVES_FORMS)

        # Create shelves
        store_shelves = []

        for index, form in enumerate(SHELVES_FORMS):
            store_shelves.append(Shelf(25, 50 + (225 * index), form.get_num_floors(), form.get_num_spaces(), form.is_double_shelf(), self.amount_floors, (index + 1), self.store_index, parent))

        SHELVES.append(store_shelves)
        SHELVES_FORMS.clear()

        # Create default form and hide it
        ShelfForm.create(parent, window)
        ShelfForm.hide_all_forms(SHELVES_FORMS)

    def init_ui(self, pos_x: int, pos_y: int, store_name: str, store_icon: str, parent):
        ## INITIALIZE OBJECTS ##
        # Buttons
        self.return_to_store_button = QPushButton(Language.get("go_back"), parent)
        self.return_to_store_button.setGeometry(1260, 10, 140, 50)
        self.return_to_store_button.hide()

        self.store_icon = ImageButton(store_name, store_icon, parent)
        self.store_icon.setGeometry(pos_x, pos_y, 150, 150)

        # Others
        self.floor_selector = QComboBox(parent)
        self.floor_selector.setGeometry(25, 10, 125, 30)

        for index in range(self.amount_floors):
            self.floor_selector.addItem(Language.get("floor") + str(index + 1))

        ## STYLE ##
        # Buttons
        self.return_to_store_button.setFont(FONT_SMALL_TEXT)
        self.return_to_store_button.setStyleSheet(DEFAULT_BUTTON)

        # Others
        self.floor_selector.setFont(FONT_SMALL_TEXT)
        self.floor_selector.setStyleSheet(COMBO_BOX)

    def init_events(self):
        self.store_icon.clicked.connect(self.open_store)
        self.return_to_store_button.clicked.connect(self.open_store)
        self.floor_selector.currentTextChanged.connect(self.change_floor)

        window.scroll.verticalScrollBar().valueChanged.connect(self.update_floor_selector_y)
        window.scroll.horizontalScrollBar().valueChanged.connect(self.update_floor_selector_x)

    def open_store(self):
        self.hide_all_store_icons(STORES)

        self.return_to_store_button.hide()

        window.hide_main_buttons()

        self.floor_selector.show()

        # Resize the scroll, so all shelves fit in the window (update vertical scroll)
        amount_shelves = len(SHELVES[self.store_index])
        window.resize_scroll_height(amount_shelves * 225 - 100)

        # Resize the scroll, so all spaces fit in the window (update horizontal scroll)
        max_amount_spaces_in_shelf = Shelf.get_max_amount_spaces_in_shelf_from_store(SHELVES[self.store_index])
        window.resize_horizontal_scroll(max_amount_spaces_in_shelf * 75 + 25)

        self.change_floor(self.floor_selector.currentText())

    def change_floor(self, floor: str):
        if floor.strip() != "":
            Shelf.change_floor(SHELVES[self.store_index], int(floor.split(' ')[1]))

    def update_floor_selector_y(self, value):
        self.floor_selector.move(self.floor_selector.pos().x(), value + 15)

        self.floor_selector.raise_()

    def update_floor_selector_x(self, value):
        self.floor_selector.move(value + 15, self.floor_selector.pos().y())

        self.floor_selector.raise_()

    def hide_store(self):
        Shelf.hide_all_spaces(SHELVES)

        self.floor_selector.hide()

    def show_icon(self):
        self.store_icon.show()

    def raise_icon(self):
        self.store_icon.raise_()

    def hide_icon(self):
        self.store_icon.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_variables()
        self.init_ui(self.widget)
        self.init_events()

        Store.show_all_store_icons(STORES)

        self.raise_main_buttons()

        self.setCentralWidget(self.scroll)
        self.resize_scroll_height()

    def init_variables(self):
        self._image = DEFAULT_IMAGE

        # Window config
        self.setWindowTitle(Language.get("window_title"))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add scroll to window
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

        shortcut_space = Space(0, 0, 0, 0, 0, 0, 0, 0)
        self.shortcut_category = CategorySpace(shortcut_space, self.widget, True)

    def init_ui(self, parent):
        ## INITIALIZE OBJECTS ##
        # Generic labels in form create store
        self.background_header_form = QLabel("", parent)
        self.background_header_form.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.background_header_form.hide()

        self.background_footer_form = QLabel("", parent)
        self.background_footer_form.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.background_footer_form.hide()

        self.label_input_store_name = QLabel(Language.get("name_store"), parent)
        self.label_input_store_name.setGeometry(400, 20, 200, 35)
        self.label_input_store_name.hide()

        # Buttons
        self.reopen_home_button = QPushButton(Language.get("go_back"), parent)
        self.reopen_home_button.setGeometry(1260, 10, 140, 50)
        self.reopen_home_button.hide()

        self.button_open_new_store_form = QPushButton(Language.get("add_store"), parent)

        self.edit_categories_button = QPushButton(Language.get("edit_categories"), parent)

        # Generic buttons in form create store
        self.add_shelf_button = QPushButton(Language.get("add_shelf"), parent)
        self.add_shelf_button.setGeometry(400, WINDOW_HEIGHT - 62, 200, 50)
        self.add_shelf_button.hide()

        self.create_store_button = QPushButton(Language.get("create_store"), parent)
        self.create_store_button.setGeometry(845, WINDOW_HEIGHT - 62, 200, 50)
        self.create_store_button.hide()

        # Generic inputs in form create store
        self.store_name_input = QLineEdit(parent)
        self.store_name_input.setGeometry(690, 10, 355, 50)
        self.store_name_input.setPlaceholderText(Language.get("store") + str(1))
        self.store_name_input.hide()

        self.icon_new_store_button = ImageButton(Language.get("change_image"), DEFAULT_IMAGE, parent)
        self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
        self.icon_new_store_button.hide()

        self.set_default_icon_button = ImageButton(Language.get("default_image"), DEFAULT_IMAGE, parent)
        self.set_default_icon_button.setGeometry(int(WINDOW_WIDTH / 2) + 25, 115, 225, 150)
        self.set_default_icon_button.hide()

        # Others
        self.language_selector = LanguageChanger(self, parent)
        self.language_selector.setGeometry(15, WINDOW_HEIGHT - 50, 100, 30)

        ## STYLE ##
        # Generic labels in form create store
        self.label_input_store_name.setFont(FONT_TEXT)

        self.background_footer_form.setStyleSheet(BACKGROUND_GREY)

        self.background_header_form.setStyleSheet(BACKGROUND_GREY)

        # Buttons
        self.button_open_new_store_form.setFont(FONT_TEXT)
        self.button_open_new_store_form.setStyleSheet(BLUE_BUTTON)

        self.reopen_home_button.setFont(FONT_SMALL_TEXT)
        self.reopen_home_button.setStyleSheet(DEFAULT_BUTTON)

        self.edit_categories_button.setFont(FONT_SMALL_TEXT)
        self.edit_categories_button.setStyleSheet(EDIT_BUTTON)

        # Generic buttons in form create store
        self.add_shelf_button.setFont(FONT_TEXT)
        self.add_shelf_button.setStyleSheet(BLUE_BUTTON)

        self.create_store_button.setFont(FONT_BIG_TEXT)
        self.create_store_button.setStyleSheet(IMPORTANT_ACTION_BUTTON)

        # Generic inputs in form create store
        self.store_name_input.setFont(FONT_SMALL_TEXT)
        self.store_name_input.setStyleSheet(INPUT_TEXT)

    def init_events(self):
        # Click buttons
        self.reopen_home_button.clicked.connect(self.reopen_home)
        self.add_shelf_button.clicked.connect(self.create_shelf_form)
        self.icon_new_store_button.clicked.connect(self.upload_image)
        self.create_store_button.clicked.connect(self.save_store_form_info)
        self.edit_categories_button.clicked.connect(self.open_config_categories)
        self.button_open_new_store_form.clicked.connect(self.open_add_store_form)
        self.set_default_icon_button.clicked.connect(self.set_default_store_icon)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.update_vertical_pos)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.update_horizontal_pos)

    def reopen_home(self):
        self.shortcut_category.hide_ui()

        self.hide_add_store_form()
        self.show_main_buttons()

        Store.hide_all_stores()
        Shelf.hide_all_spaces(SHELVES)
        Store.show_all_store_icons(STORES)
        ShelfForm.hide_all_forms(SHELVES_FORMS)

        self.raise_main_buttons()
        self.resize_main()

    def hide_add_store_form(self):
        self.set_default_icon_button.hide()
        self.background_header_form.hide()
        self.background_footer_form.hide()
        self.label_input_store_name.hide()
        self.icon_new_store_button.hide()
        self.create_store_button.hide()
        self.reopen_home_button.hide()
        self.store_name_input.hide()
        self.add_shelf_button.hide()
    
    def show_main_buttons(self):
        self.language_selector.show()
        self.edit_categories_button.show()
        self.button_open_new_store_form.show()

    def raise_main_buttons(self):
        self.language_selector.raise_()
        self.button_open_new_store_form.raise_()
        self.edit_categories_button.raise_()

    def resize_main(self):
        if len(STORES) < 25:
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        else:
            self.widget.resize(WINDOW_WIDTH - 20, STORES[len(STORES) - 1].store_icon.pos().y() + 290)

    def create_shelf_form(self):
        ShelfForm.create(self.widget, self)
    
        self.resize_scroll_height()
    
    def resize_scroll_height(self, height = 0):
        if height == 0:
            if len(SHELVES_FORMS) > 0 and SHELVES_FORMS[len(SHELVES_FORMS) - 1].pos().y() + 300 > WINDOW_HEIGHT:
                self.widget.resize(WINDOW_WIDTH - 20, SHELVES_FORMS[len(SHELVES_FORMS) - 1].pos().y() + 300)
            else:
                self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

            self.raise_shelf_footer_form()
        else:
            width = WINDOW_WIDTH - 5
            aux = height + 175

            if aux > WINDOW_HEIGHT - 5:
                width -= 15

            self.widget.resize(width, aux)
    
    def raise_shelf_footer_form(self):
        self.background_footer_form.raise_()
        self.create_store_button.raise_()
        self.add_shelf_button.raise_()

    def upload_image(self):
        # Open a file dialog to select an image file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        
        # Check if a file was selected
        if file_path:
            self._image = file_path
            self.icon_new_store_button.setPixmap(self._image)

            if self._image != DEFAULT_IMAGE:
                self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 150, 115, 150, 150)
                self.set_default_icon_button.show()
            else:
                self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
                self.set_default_icon_button.hide()

    def save_store_form_info(self):
        save_shelves_info(SHELVES_FORMS)

        store_name = self.store_name_input.text().strip()

        if len(store_name) <= 15:
            if store_name == "":
                store_name = Language.get("store") + str(len(STORES) + 1)

            if UserManager.get_role() != 'Offline':
                Store.create_mongo_store(store_name, self._image)

            ShelfForm.hide_all_forms(SHELVES_FORMS)
            Store.create_store(store_name, self.widget, self._image)

            self.store_name_input.setText("")
            self.store_name_input.setPlaceholderText(Language.get("store") + str(len(STORES) + 1))

            self.reopen_home()
            self.reopen_home_button.raise_()
        else:
            QMessageBox.warning(None, "Name too long", "The store name must be maximum 15 digits long")

    def open_config_categories(self):
        Store.hide_all_store_icons()

        self.shortcut_category.show_ui()

        self.hide_main_buttons()

    def hide_main_buttons(self):
        self.button_open_new_store_form.hide()
        self.edit_categories_button.hide()
        self.language_selector.hide()

        self.reopen_home_button.show()

    def open_add_store_form(self):
        self.show_add_store_form()
        self.resize_scroll_height()
        
        if len(SHELVES_FORMS) == 0:
            self.create_shelf_form()

        ShelfForm.show_all_forms(SHELVES_FORMS)
        Store.hide_all_store_icons(STORES)

        self.button_open_new_store_form.hide()
        self.edit_categories_button.hide()
        self.language_selector.hide()

        self.reopen_home_button.show()

        self.reopen_home_button.raise_()
    
    def show_add_store_form(self):
        self.background_header_form.show()
        self.background_footer_form.show()
        self.label_input_store_name.show()
        self.icon_new_store_button.show()
        self.create_store_button.show()
        self.store_name_input.show()
        self.add_shelf_button.show()

        if self._image != DEFAULT_IMAGE:
            self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 175, 115, 150, 150)
            self.set_default_icon_button.show()
        else:
            self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
            self.set_default_icon_button.hide()

    def set_default_store_icon(self):
        self._image = DEFAULT_IMAGE

        self.icon_new_store_button.setPixmap(self._image)
        self.icon_new_store_button.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)

        self.set_default_icon_button.hide()

    def update_vertical_pos(self, value):
        self.store_name_input.move(self.store_name_input.pos().x(), value + 10)
        self.reopen_home_button.move(self.reopen_home_button.pos().x(), value + 10)
        self.background_header_form.move(self.background_header_form.pos().x(), value)
        self.label_input_store_name.move(self.label_input_store_name.pos().x(), value + 20)
        self.add_shelf_button.move(self.add_shelf_button.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.create_store_button.move(self.create_store_button.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.language_selector.move(self.language_selector.pos().x() + 15, value + (WINDOW_HEIGHT - 50))
        self.background_footer_form.move(self.background_footer_form.pos().x(), value + (WINDOW_HEIGHT - 75))
        self.edit_categories_button.move(self.edit_categories_button.pos().x(), value + (WINDOW_HEIGHT - 115))
        self.button_open_new_store_form.move(self.button_open_new_store_form.pos().x(), value + (WINDOW_HEIGHT - 75))

        self.raise_store_header_form()

    def raise_store_header_form(self):
        self.background_header_form.raise_()
        self.label_input_store_name.raise_()
        self.reopen_home_button.raise_()
        self.store_name_input.raise_()

    def update_horizontal_pos(self, value):
        self.reopen_home_button.move(value + 1300, self.reopen_home_button.pos().y())

    def resize_horizontal_scroll(self, width = WINDOW_WIDTH):
        if width < WINDOW_WIDTH:
            self.widget.resize(self.widget.width(), self.widget.height())
        else:
            self.widget.resize(width + 125, self.widget.height())

    def hide_all_buttons(self):
        self.button_open_new_store_form.hide()
        self.edit_categories_button.hide()
        self.reopen_home_button.hide()
        self.language_selector.hide()

    def change_user_role(self, role, username = ''):
        if role != 'Offline':
            UserManager.set_user(username, role)

        if UserManager.get_role() == 'Offline' or UserManager.get_role() == 'Manager':
            self.button_open_new_store_form.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 75, 190, 50)
            self.edit_categories_button.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 115, 190, 30)
        else:
            self.button_open_new_store_form.setGeometry(0, 0, 0, 0)
            self.edit_categories_button.setGeometry(0, 0, 0, 0)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if UserManager.get_role() == 'Offline' or UserManager.get_role() == 'Manager':
                        space.edit_categories_button.setGeometry(320, 26, 26, 26)
                    else:
                        space.edit_categories_button.setGeometry(0, 0, 0, 0)

window = MainWindow()

class main():
    log_in_window = LogInWindow(window)
    log_in_window.show()

    sys.exit(app.exec_())

    DB.close_connection()

if __name__ == "__main__":
    main()
