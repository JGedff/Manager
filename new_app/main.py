import os
import sys
import time
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
            window.hideAllButtons()
        else:
            Store.hideAllStores()

    def hide_ui(self):
        for category_button in self.categories_buttons:
            category_button.hide()

        self.add_category_button.hide()

        if self._shortcut:
            self.cancel_add_category()
            window.goHome.show()

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

    def update_categories_name(self, updated_name):
        index = Category.get_index_by_name(self._name_modified_categoy)
        Category.change_category_name(index, updated_name)

        update_category_name(window.shortcut_category, self._color_modified_category, self._name_modified_categoy, updated_name, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    update_category_name(space, self._color_modified_category, self._name_modified_categoy, updated_name)

    def update_categories_color(self, category_name):
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
            window.hideMainButtons()
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
    def __init__(self, pos_x, pos_y, actual_floor, shelf_floors, store_i, shelf_i, space_i, parent = None, long = False):
        super().__init__(parent)

        self.setGeometry(pos_x, pos_y, 75, 75)

        self.init_variables(actual_floor, shelf_floors, store_i, shelf_i, parent, long)
        self.init_ui(space_i, parent)
        self.init_events()

    def init_variables(self, actual_floor, shelf_floors, store_i, shelf_i, parent, long):
        self._long = long
        self.mongo_id = None
        self._store_i = store_i
        self._actual_floor = actual_floor
        self.shelf_i = shelf_i
        self.category = CategorySpace(self, parent)
        update_category_buttons_pos(self.category)

        if actual_floor > shelf_floors:
            set_unreachable_category(self.category)

    def init_ui(self, space_i, parent):
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

        self.updateSpaceColor()

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

    def updateSpaceColor(self):
        self.box.setStyleSheet(get_style_sheet(self.category.color))
        self.space_number.setStyleSheet(get_style_sheet(self.category.color))

    def init_events(self):
        self.box.clicked.connect(self.configSpace)
        self.return_to_space_config.clicked.connect(self.stopConfigSpace)
        self.edit_categories_button.clicked.connect(self.openConfigCategories)
        self.category_selector.currentTextChanged.connect(self.changeCategory)

    def configSpace(self):
        window.hideAllButtons()

        Store.hideAllStores()
        Store.configSpace(self._store_i)

        self.box.hide()

        self.space_number.show()
        self.shelf_number.show()
        self.label_category_selected.show()
        self.edit_categories_button.show()
        self.category_selector.show()
        self.label_can_hold_product.show()
        self.category_can_hold_product.show()
    
        if hasattr(self, "product"):
            self.product.show()
        
        window.resize_scroll_height()
            
    def openConfigCategories(self):
        if hasattr(self, "product"):
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.showHideCreateProduct()

        Store.configCategory(self._store_i)

        window.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

        self.space_number.hide()
        self.shelf_number.hide()
        self.label_category_selected.hide()
        self.edit_categories_button.hide()
        self.category_selector.hide()
        self.label_can_hold_product.hide()
        self.category_can_hold_product.hide()

        if hasattr(self, "product"):
            self.product.hide()

        self.return_to_space_config.show()
        self.category.show_ui()

    def stopConfigSpace(self):
        self.updateSpaceColor()

        self.category.cancelAddCategory()

        ShelfInfo.hideAllSpaces()

        Store.stopConfigCategory(self._store_i)

        self.space_number.show()
        self.shelf_number.show()
        self.label_category_selected.show()
        self.edit_categories_button.show()
        self.category_selector.show()
        self.label_can_hold_product.show()
        self.category_can_hold_product.show()

        if hasattr(self, "product"):
            self.product.show()

        self.return_to_space_config.hide()
    
    def changeCategory(self, category):
        oldName = self.category.name

        set_category_by_name(self.category, category)
        self.updateSpaceColor()

        if Category.categoryCanHoldProduct(category):
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
            Mongo.update_category_space(self.mongo_id, oldName)

    def updateVerticalHeaderPosition(self, value):
        self.return_to_space_config.move(self.return_to_space_config.pos().x(), value + 15)

    def showFloor(self, number):
        if number != self._actual_floor:
            self.hideSpace()
        else:
            self.showSpace()

    def hideSpace(self):
        self.box.hide()
        self.space_number.hide()
        self.shelf_number.hide()
        self.label_category_selected.hide()
        self.edit_categories_button.hide()
        self.return_to_space_config.hide()
        self.category_selector.hide()
        self.label_can_hold_product.hide()
        self.category_can_hold_product.hide()

        if hasattr(self, "product"):
            self.product.hide()
        
        self.category.hide_ui()

    def showSpace(self):
        self.updateSpaceColor()

        self.box.show()

        self.space_number.hide()
        self.shelf_number.hide()
        self.label_category_selected.hide()
        self.edit_categories_button.hide()
        self.return_to_space_config.hide()
        self.category_selector.hide()
        self.label_can_hold_product.hide()
        self.category_can_hold_product.hide()

        if hasattr(self, "product"):
            if self.product.creating_product:
                self.product.showHideCreateProduct()

            self.product.hide()

        self.box.raise_()

class ShelfInfo():
    @staticmethod
    def hideSpaces(shelf):
        shelf.shelfNumber.hide()

        for space in shelf.spaces:
            space.hideSpace()

    @staticmethod
    def hideAllSpaces():
        for stores in SHELVES:
            for shelf in stores:
                shelf.shelfNumber.hide()

                for space in shelf.spaces:
                    space.hideSpace()
    
    @staticmethod
    def changeFloor(index, number):
        for shelf in SHELVES[index]:
            shelf.shelfNumber.show()

            for space in shelf.spaces:
                space.showFloor(number)
    
    @staticmethod
    def getMaxSpaces(index):
        maxSpaces = 1

        for shelf in SHELVES[index]:
            numSpaces = shelf.spaces.__len__()

            if shelf.double_shelf:
                numSpaces = int(numSpaces / 2)

            if numSpaces > maxSpaces:
                maxSpaces = numSpaces

        return maxSpaces

    def __init__(self, posx, posy, floors, spaces, double_shelf, storeFloors, shelfNumber = 1, storeIndex = 1, parent = None):
        self.initVariables(posx, floors, spaces, double_shelf, storeFloors, shelfNumber, storeIndex)
        self.initUI(posx, posy, parent)
        self.initEvents()
    
    def initVariables(self, posx, floors, spaces, double_shelf, storeFloors, shelfNumber, storeIndex):
        self.spaces = []
        self.posx = posx
        self.floors = floors
        self.spacesLength = spaces
        self.storeIndex = storeIndex
        self.storeFloors = storeFloors
        self.actualNumber = shelfNumber
        self.double_shelf = double_shelf

    def initUI(self, posx, posy, parent):
        self.shelfNumber = QLabel(Language.get("shelf") + str(self.actualNumber) + ":", parent)
        self.shelfNumber.setGeometry(int(WINDOW_WIDTH / 2 - 125 / 2), posy, 125, 25)
        self.shelfNumber.hide()

        posy += 35

        for actualFloor in range(self.storeFloors):
            times5 = 0

            if self.double_shelf:
                indexSpace = 0
                mod = self.spacesLength % 2
                sideSpaces = (self.spacesLength / 2).__trunc__()

                for index in range(sideSpaces):
                    if (index + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, indexSpace, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, indexSpace, parent, False, times5))

                    indexSpace += 1

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (75 * index), posy + 75, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, indexSpace, parent))
                    indexSpace += 1
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (75 * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, indexSpace, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, indexSpace, parent, True, times5))

                    indexSpace += 1
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent, False, times5))

        self.shelfNumber.setFont(FONT_TEXT)

    def initEvents(self):
        update_shelves_pos(SHELVES_FORMS)
        window.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalInfoPosition)

    def updateHorizontalInfoPosition(self, value):
        self.shelfNumber.move(value + int(WINDOW_WIDTH / 2 - self.shelfNumber.width() / 2), self.shelfNumber.pos().y())

class Store():
    @staticmethod
    def createMongoStore(name, image = DEFAULT_IMAGE):
        image_path = image

        if image != DEFAULT_IMAGE:
            # Copy the uploaded image to the save directory
            save_dir = "img"
            os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

            file_name = os.path.basename(image)
            save_path = os.path.join(save_dir, file_name)
            image_path = save_path

            shutil.copy(image, save_path)

        shelvesInfo = []
        mongo_id = 0

        storeFloors = get_max_floor(SHELVES_FORMS)
        emptyCategory = get_empty_category_name()
        unreachableCategory = get_unreachable_category_name()
        id_empty_category = Mongo.get_category_by_name(emptyCategory)
        id_unreachable_category = Mongo.get_category_by_name(unreachableCategory)

        for form in SHELVES_FORMS:
            spacesInfo = []

            time.sleep(0.01)

            for floor in range(storeFloors):
                for _ in range(form.get_num_spaces()):
                    id_category = id_unreachable_category if form.get_num_floors() - 1 < floor else id_empty_category 

                    spacesInfo.append({
                        "category": id_category,
                        "mongo_id": name + "_" + str(mongo_id),
                        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    })

                    mongo_id += 1
            
            shelvesInfo.append({
                "floors": form.get_num_floors(),
                "spaces": spacesInfo,
                "double_shelf": form.is_double_shelf(),
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            })
            
        Mongo.add_store(shelvesInfo, name, image_path)

    @staticmethod
    def createStore(storeName, parent, image = DEFAULT_IMAGE):
        posx = 25
        posy = 25
            
        for _ in STORES:
            posx += 170

            if posx + 170 >= WINDOW_WIDTH:
                posx = 25
                posy += 170

        STORES.append(Store(storeName, image, posx, posy, parent))

        SHELVES_FORMS.clear()
    
    @staticmethod
    def hideAllStoreIcons():
        for store in STORES:
            store.hide_icon()

    @staticmethod
    def showAllStoreIcons():
        for store in STORES:
            store.show_icon()
            store.raise_icon()

    @staticmethod
    def hideAllStores():
        for store in STORES:
            store.hideStore()

    @staticmethod
    def configSpace(indexStore):
        STORES[indexStore].changeFloorButton.hide()
        STORES[indexStore].goBackStore.show()

    @staticmethod
    def configCategory(indexStore):
        STORES[indexStore].goBackStore.hide()

    @staticmethod
    def stopConfigCategory(indexStore):
        STORES[indexStore].goBackStore.show()

    def __init__(self, name, image, posx, posy, parent):
        self.setupStore(parent)
        self.initUI(name, image, posx, posy, parent)
        self.initEvents()
    
    def setupStore(self, parent):
        self.indexShelves = SHELVES.__len__()
        self.floor = get_max_floor(SHELVES_FORMS)
        storeShelves = []

        for index, form in enumerate(SHELVES_FORMS):
            storeShelves.append(ShelfInfo(25, 50 + (225 * index), form.floors, form.spaces, form.double_shelf, self.floor, (index + 1), STORES.__len__(), parent))
        
        SHELVES.append(storeShelves)
        SHELVES_FORMS.clear()
        
        ShelfForm.create(parent, window)
        ShelfForm.hide_all_forms()

    def initUI(self, name, image, posx, posy, parent):
        self.goBackStore = QPushButton(Language.get("go_back"), parent)
        self.goBackStore.setGeometry(1260, 10, 140, 50)
        self.goBackStore.hide()

        self.store_icon = ImageButton(name, image, parent)
        self.store_icon.setGeometry(posx, posy, 150, 150)

        self.changeFloorButton = QComboBox(parent)
        self.changeFloorButton.setGeometry(25, 10, 125, 30)

        for index in range(self.floor):
            self.changeFloorButton.addItem(Language.get("floor") + str(index + 1))

        self.goBackStore.setFont(FONT_SMALL_TEXT)
        self.changeFloorButton.setFont(FONT_SMALL_TEXT)

        self.goBackStore.setStyleSheet(DEFAULT_BUTTON)
        self.changeFloorButton.setStyleSheet(COMBO_BOX)

    def initEvents(self):
        self.store_icon.clicked.connect(self.openStore)
        self.goBackStore.clicked.connect(self.openStore)
        self.changeFloorButton.currentTextChanged.connect(self.changeFloor)

        window.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        window.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)

    def openStore(self):
        amountShelves = SHELVES[self.indexShelves].__len__()
        amountSpaces = ShelfInfo.getMaxSpaces(self.indexShelves)

        self.hideAllStoreIcons()

        self.goBackStore.hide()

        window.hideMainButtons()
        window.resize_scroll_height(amountShelves * 225 - 100)
        window.resizeWidthScroll(amountSpaces * 75 + 25)

        self.changeFloorButton.show()
        self.changeFloor(self.changeFloorButton.currentText())

    def changeFloor(self, floor):
        if floor.strip() != "":
            ShelfInfo.changeFloor(self.indexShelves, int(floor.split(' ')[1]))

    def updateVerticalHeaderPosition(self, value):
        self.changeFloorButton.move(self.changeFloorButton.pos().x(), value + 15)

        self.changeFloorButton.raise_()

    def updateHorizontalHeaderPosition(self, value):
        self.changeFloorButton.move(value + 15, self.changeFloorButton.pos().y())

        self.changeFloorButton.raise_()

    def hideStore(self):
        ShelfInfo.hideAllSpaces()

        self.changeFloorButton.hide()

    def show_icon(self):
        self.store_icon.show()

    def raise_icon(self):
        self.store_icon.raise_()

    def hide_icon(self):
        self.store_icon.hide()

    def configCategories(self):
        self.goBackStore.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initVariables()
        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resize_scroll_height()

    def initVariables(self):
        self.image = DEFAULT_IMAGE

        # Window config
        self.setWindowTitle(Language.get("window_title"))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add scroll to window
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

        shortcut = Space(0, 0, 0, 0, 0, 0, 0, 0)
        self.shortcut_category = CategorySpace(shortcut, self.widget, True)

    def initUI(self, parent):
        # Main buttons
        self.goHome = QPushButton(Language.get("go_back"), parent)
        self.goHome.setGeometry(1260, 10, 140, 50)
        self.goHome.hide()

        self.addStoreButton = QPushButton(Language.get("add_store"), parent)
        self.edit_categories_button = QPushButton(Language.get("edit_categories"), parent)

        self.languageChanger = LanguageChanger(self, parent)
        self.languageChanger.setGeometry(15, WINDOW_HEIGHT - 50, 100, 30)
        
        # Header Form
        self.headerFormBackground = QLabel("", parent)
        self.headerFormBackground.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.headerFormBackground.setStyleSheet(BACKGROUND_GREY)
        self.headerFormBackground.hide()

        self.storeNameLabel = QLabel(Language.get("name_store"), parent)
        self.storeNameLabel.setGeometry(400, 20, 200, 35)
        self.storeNameLabel.hide()
        
        self.store_name_input = QLineEdit(parent)
        self.store_name_input.setGeometry(690, 10, 355, 50)
        self.store_name_input.setPlaceholderText(Language.get("store") + str(1))
        self.store_name_input.hide()

        # Body form
        self.icon_new_store = ImageButton(Language.get("change_image"), DEFAULT_IMAGE, parent)
        self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
        self.icon_new_store.hide()

        self.setDefaultIcon = ImageButton(Language.get("default_image"), DEFAULT_IMAGE, parent)
        self.setDefaultIcon.setGeometry(int(WINDOW_WIDTH / 2) + 25, 115, 225, 150)
        self.setDefaultIcon.hide()

        # Footer form
        self.footerFormBackground = QLabel("", parent)
        self.footerFormBackground.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.footerFormBackground.setStyleSheet(BACKGROUND_GREY)
        self.footerFormBackground.hide()

        self.addShelfButton = QPushButton(Language.get("add_shelf"), parent)
        self.addShelfButton.setGeometry(400, WINDOW_HEIGHT - 62, 200, 50)
        self.addShelfButton.hide()

        self.createStoreButton = QPushButton(Language.get("create_store"), parent)
        self.createStoreButton.setGeometry(845, WINDOW_HEIGHT - 62, 200, 50)
        self.createStoreButton.hide()

        # Style
        self.createStoreButton.setFont(FONT_BIG_TEXT)

        self.addStoreButton.setFont(FONT_TEXT)
        self.storeNameLabel.setFont(FONT_TEXT)
        self.addShelfButton.setFont(FONT_TEXT)

        self.goHome.setFont(FONT_SMALL_TEXT)
        self.edit_categories_button.setFont(FONT_SMALL_TEXT)
        self.store_name_input.setFont(FONT_SMALL_TEXT)

        self.goHome.setStyleSheet(DEFAULT_BUTTON)
        self.store_name_input.setStyleSheet(INPUT_TEXT)
        self.addStoreButton.setStyleSheet(BLUE_BUTTON)
        self.edit_categories_button.setStyleSheet(EDIT_BUTTON)
        self.addShelfButton.setStyleSheet(BLUE_BUTTON)
        self.createStoreButton.setStyleSheet(IMPORTANT_ACTION_BUTTON)

        Store.showAllStoreIcons()

        self.raiseMainButtons()

    def initEvents(self):
        # Click buttons
        self.goHome.clicked.connect(self.re_open_home)
        self.addStoreButton.clicked.connect(self.addStore)
        self.addShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.saveStoreInfo)
        self.edit_categories_button.clicked.connect(self.configCategories)
        self.icon_new_store.clicked.connect(self.uploadImage)
        self.setDefaultIcon.clicked.connect(self.setDefaultStoreIcon)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)
    
    # Scroll functions
    def updateVerticalHeaderPosition(self, value):
        self.goHome.move(self.goHome.pos().x(), value + 10)
        self.edit_categories_button.move(self.edit_categories_button.pos().x(), value + (WINDOW_HEIGHT - 115))
        self.store_name_input.move(self.store_name_input.pos().x(), value + 10)
        self.storeNameLabel.move(self.storeNameLabel.pos().x(), value + 20)
        self.headerFormBackground.move(self.headerFormBackground.pos().x(), value)
        self.addStoreButton.move(self.addStoreButton.pos().x(), value + (WINDOW_HEIGHT - 75))
        self.addShelfButton.move(self.addShelfButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.createStoreButton.move(self.createStoreButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.languageChanger.move(self.languageChanger.pos().x() + 15, value + (WINDOW_HEIGHT - 50))
        self.footerFormBackground.move(self.footerFormBackground.pos().x(), value + (WINDOW_HEIGHT - 75))

        self.raiseShelfHeaderForm()

    def updateHorizontalHeaderPosition(self, value):
        self.goHome.move(value + 1300, self.goHome.pos().y())

    # Resize scroll functions
    def resize_scroll_height(self, height = 0):
        if height == 0:
            if SHELVES_FORMS.__len__() > 0 and SHELVES_FORMS[SHELVES_FORMS.__len__() - 1].pos().y() + 300 > WINDOW_HEIGHT:
                self.widget.resize(WINDOW_WIDTH - 20, SHELVES_FORMS[SHELVES_FORMS.__len__() - 1].pos().y() + 300)
            else:
                self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

            self.raiseShelfFooterForm()
        else:
            width = WINDOW_WIDTH - 5
            aux = height + 175

            if aux > WINDOW_HEIGHT - 5:
                width -= 15

            self.widget.resize(width, aux)

    def resizeWidthScroll(self, width = WINDOW_WIDTH):
        if width < WINDOW_WIDTH:
            self.widget.resize(self.widget.width(), self.widget.height())
        else:
            self.widget.resize(width + 125, self.widget.height())

    def resizeMain(self):
        if STORES.__len__() < 25:
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        else:
            self.widget.resize(WINDOW_WIDTH - 20, STORES[STORES.__len__() - 1].store_icon.pos().y() + 290)

    # UI functions
    def re_open_home(self):
        self.shortcut_category.hide_ui()

        self.showMainButtons()
        self.hideAddStoreForm()
        self.raiseMainButtons()

        ShelfForm.hide_all_forms()
        Store.hideAllStores()
        Store.showAllStoreIcons()
        ShelfInfo.hideAllSpaces()

        self.raiseMainButtons()
        self.resizeMain()

    def addStore(self):
        self.showAddStoreForm()
        self.resize_scroll_height()
        
        if SHELVES_FORMS.__len__() == 0:
            self.createShelf()

        ShelfForm.show_all_forms()
        Store.hideAllStoreIcons()

        self.goHome.show()
        self.goHome.raise_()
        self.addStoreButton.hide()
        self.edit_categories_button.hide()
        self.languageChanger.hide()

    def createShelf(self):
        ShelfForm.create(self.widget, self)
    
        self.resize_scroll_height()

    def saveStoreInfo(self):
        save_shelves_info(SHELVES_FORMS)

        storeName = self.store_name_input.text().strip()

        if storeName.__len__() <= 15:
            if storeName == "":
                storeName = Language.get("store") + str(STORES.__len__() + 1)

            if UserManager.get_role() != 'Offline':
                Store.createMongoStore(storeName, self.image)

            ShelfForm.hide_all_forms()
            Store.createStore(storeName, self.widget, self.image)

            self.store_name_input.setText("")
            self.store_name_input.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))

            self.re_open_home()
            self.goHome.raise_()
        else:
            QMessageBox.warning(None, "Name too long", "The store name must be maximum 15 digits long")
    
    def configCategories(self):
        Store.hideAllStoreIcons()

        self.shortcut_category.show_ui()

        self.hideMainButtons()

    def uploadImage(self):
        # Open a file dialog to select an image file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        
        # Check if a file was selected
        if file_path:
            self.image = file_path
            self.icon_new_store.setPixmap(self.image)

            if self.image != DEFAULT_IMAGE:
                self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 150, 115, 150, 150)
                self.setDefaultIcon.show()
            else:
                self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
                self.setDefaultIcon.hide()

    def setDefaultStoreIcon(self):
        self.image = DEFAULT_IMAGE
        self.icon_new_store.setPixmap(self.image)
        self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
        self.setDefaultIcon.hide()

    # Show objects
    def showAddStoreForm(self):
        self.headerFormBackground.show()
        self.footerFormBackground.show()
        self.createStoreButton.show()
        self.store_name_input.show()
        self.storeNameLabel.show()
        self.addShelfButton.show()
        self.icon_new_store.show()

        if self.image != DEFAULT_IMAGE:
            self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 175, 115, 150, 150)
            self.setDefaultIcon.show()
        else:
            self.icon_new_store.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
            self.setDefaultIcon.hide()

    def showMainButtons(self):
        self.languageChanger.show()
        self.edit_categories_button.show()
        self.addStoreButton.show()

    # Hide objects
    def hideAddStoreForm(self):
        self.headerFormBackground.hide()
        self.footerFormBackground.hide()
        self.createStoreButton.hide()
        self.store_name_input.hide()
        self.storeNameLabel.hide()
        self.addShelfButton.hide()
        self.setDefaultIcon.hide()
        self.icon_new_store.hide()
        self.goHome.hide()

    def hideAllButtons(self):
        self.goHome.hide()
        self.addStoreButton.hide()
        self.edit_categories_button.hide()
        self.languageChanger.hide()

    # Hide and show objects
    def hideMainButtons(self):
        self.goHome.show()
        self.addStoreButton.hide()
        self.edit_categories_button.hide()
        self.languageChanger.hide()

    # Raise objects
    def raiseShelfFooterForm(self):
        self.footerFormBackground.raise_()
        self.createStoreButton.raise_()
        self.addShelfButton.raise_()

    def raiseShelfHeaderForm(self):
        self.headerFormBackground.raise_()
        self.store_name_input.raise_()
        self.storeNameLabel.raise_()
        self.goHome.raise_()
    
    def raiseMainButtons(self):
        self.languageChanger.raise_()
        self.addStoreButton.raise_()
        self.edit_categories_button.raise_()

    def change_user_role(self, role, username = ''):
        if role != 'Offline':
            UserManager.setUser(username, role)

        if UserManager.get_role() == 'Offline' or UserManager.get_role() == 'Manager':
            self.addStoreButton.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 75, 190, 50)
            self.edit_categories_button.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 115, 190, 30)
        else:
            self.addStoreButton.setGeometry(0, 0, 0, 0)
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
    logInWindow = LogInWindow(window)
    logInWindow.show()

    sys.exit(app.exec_())

    Mongo.close_connection()

if __name__ == "__main__":
    main()
