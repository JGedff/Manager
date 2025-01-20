import os
import sys
import time
import shutil
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QColorDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

from styles.style_sheets import INPUT_TEXT, DEFAULT_BUTTON, COMBO_BOX, REST_BUTTON, BLUE_BUTTON, EDIT_BUTTON, OFF_BUTTON, IMPORTANT_ACTION_BUTTON, BACKGROUND_BLACK, BACKGROUND_GREY
from styles.fonts import FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR, FONT_SMALL_BOLD_TEXT
from styles.color_functions import get_style_sheet

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS, STORES, DEFAULT_IMAGE, SHELVES, CATEGORY_NAMES

from utils.functions.global_functions import get_max_floor
from utils.functions.shelf_functions import save_shelves_info, update_shelves_pos
from utils.functions.space_category_functions import set_unreachable_category, set_category_by_name, update_category_name, delete_category_from, set_empty_category, get_unreachable_category_name, get_empty_category_name

from utils.mongoDb import Mongo
from utils.user_manager import UserManager

from utils.language import Language
from utils.category import Category

from components.product import Product
from components.log_in import LogInWindow
from components.input_bool import InputBool
from components.input_integer import InputInteger
from components.image_button import ImageButton
from components.double_button import DoubleButton
from components.language_changer import LanguageChanger

app = QApplication(sys.argv)

class SpaceCategory(QLabel):
    def __init__(self, storeIndex = 0, shelfIndex = 0, spacesInFloorShelf = 0, floor = 0, spaceIndex = 0, parent = None, shortcut = False):
        super().__init__(parent)

        self.initVariables(storeIndex, shelfIndex, spacesInFloorShelf, floor, spaceIndex, parent, shortcut)
        self.initUI(parent)
        self.initEvents()

        set_empty_category(self)

    def initVariables(self, storeIndex, shelfIndex, spacesInFloorShelf, floor, spaceIndex, parent, shortcut):
        self.name = ''
        self.color = ''
        self.newColor = ''
        self.floor = floor
        self.double_buttons = []
        self.mainParent = parent
        self.shortcut = shortcut
        self.newCategoryName = ""
        self.newCategoryColor = ""
        self.storeIndex = storeIndex
        self.shelfIndex = shelfIndex
        self.spaceIndex = spaceIndex
        self.creatingCategory = False
        self.nameModifiedCategory = ''
        self.colorModifiedCategory = ""
        self.spacesInFloorShelf = spacesInFloorShelf

    def initUI(self, parent):
        self.showSpace = QPushButton(Language.get("go_back"), parent)
        self.showSpace.setGeometry(1260, 10, 140, 50)
        self.showSpace.hide()

        # Edit existing category
        self.categoryNameLabel = QLabel(Language.get("category_name"), parent)
        self.categoryNameLabel.setGeometry(50, 60, 175, 25)
        self.categoryNameLabel.hide()

        self.categoryName = QLineEdit(parent)
        self.categoryName.setGeometry(250, 50, 250, 39)
        self.categoryName.hide()
        
        self.categoryColorLabel = QLabel(Language.get("category_color"), parent)
        self.categoryColorLabel.setGeometry(50, 110, 175, 25)
        self.categoryColorLabel.hide()

        self.categoryColor = QPushButton(Language.get("select_color"), parent)
        self.categoryColor.setGeometry(250, 100, 138, 39)
        self.categoryColor.hide()

        self.saveCategory = QPushButton(Language.get("save"), parent)
        self.saveCategory.setGeometry(250, 150, 125, 39)
        self.saveCategory.hide()

        posx = 25
        posy = 25

        for category in CATEGORY_NAMES:
            new_double_button = DoubleButton(category.capitalize(), "❌", self.edit_category_function, self.delete_category_function, parent)
            new_double_button.setGeometry(posx - 12, posy - 12, 450, 69)

            posy += 69
            self.double_buttons.append(new_double_button)

        # Adding a new category
        self.add_category_button = QPushButton(Language.get("add_category"), parent)
        self.add_category_button.setGeometry(posx + 13, posy + 13, 200, 25)
        self.add_category_button.hide()

        self.addCategoryName = QLineEdit(parent)
        self.addCategoryName.setGeometry(posx + 13, posy - 100, 250, 39)
        self.addCategoryName.setPlaceholderText(Language.get("name"))
        self.addCategoryName.hide()

        self.newCategoryColorButton = QPushButton(Language.get("select_color"), parent)
        self.newCategoryColorButton.setGeometry(posx + 238, posy - 175, 138, 39)
        self.newCategoryColorButton.hide()

        self.cancelButtonAddCategory = QPushButton(Language.get("cancel"), parent)
        self.cancelButtonAddCategory.setGeometry(posx + 13, posy, 100, 25)
        self.cancelButtonAddCategory.hide()

        self.createCategoryButton = QPushButton(Language.get("create"), parent)
        self.createCategoryButton.setGeometry(posx + 438, posy, 100, 25)
        self.createCategoryButton.setDisabled(True)
        self.createCategoryButton.hide()

        self.categoryNameLabel.setAlignment(Qt.AlignRight)
        self.categoryColorLabel.setAlignment(Qt.AlignRight)

        self.saveCategory.setFont(FONT_SMALL_BOLD_TEXT)

        self.showSpace.setFont(FONT_SMALL_TEXT)
        self.categoryName.setFont(FONT_SMALL_TEXT)
        self.categoryColor.setFont(FONT_SMALL_TEXT)
        self.addCategoryName.setFont(FONT_SMALL_TEXT)
        self.categoryNameLabel.setFont(FONT_SMALL_TEXT)
        self.categoryColorLabel.setFont(FONT_SMALL_TEXT)
        self.add_category_button.setFont(FONT_SMALL_TEXT)
        self.createCategoryButton.setFont(FONT_SMALL_TEXT)
        self.newCategoryColorButton.setFont(FONT_SMALL_TEXT)
        self.cancelButtonAddCategory.setFont(FONT_SMALL_TEXT)

        self.categoryName.setStyleSheet(INPUT_TEXT)
        self.showSpace.setStyleSheet(DEFAULT_BUTTON)
        self.addCategoryName.setStyleSheet(INPUT_TEXT)
        self.add_category_button.setStyleSheet(BLUE_BUTTON)
        self.cancelButtonAddCategory.setStyleSheet(OFF_BUTTON)
        self.saveCategory.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.categoryColor.setStyleSheet(get_style_sheet("#FFFFFF"))
        self.createCategoryButton.setStyleSheet(IMPORTANT_ACTION_BUTTON)
        self.newCategoryColorButton.setStyleSheet(get_style_sheet("#FFFFFF"))

    def initEvents(self):
        self.showSpace.clicked.connect(self.stopEditCategory)
        self.categoryColor.clicked.connect(self.selectColor)
        self.saveCategory.clicked.connect(self.saveInfo)
        self.add_category_button.clicked.connect(self.showAddCategory)
        self.cancelButtonAddCategory.clicked.connect(self.cancelAddCategory)
        self.createCategoryButton.clicked.connect(self.createCategory)
        self.newCategoryColorButton.clicked.connect(self.selectColorNewCategory)
        self.addCategoryName.textChanged.connect(self.changeNewCategoryName)

    def stopEditCategory(self):
        self.showUI()
        self.showSpace.hide()
        self.categoryNameLabel.hide()
        self.categoryColorLabel.hide()
        self.saveCategory.hide()
        self.categoryColor.hide()
        self.categoryName.hide()
        self.categoryName.setText("")

        if self.shortcut:
            window.hideMainButtons()
        else:
            SHELVES[self.storeIndex][self.shelfIndex].spaces[(self.floor - 1) * self.spacesInFloorShelf + self.spaceIndex].openSpaceConfig.show()

    def showUI(self):
        for button in self.double_buttons:
            button.show()
            button.raise_()

        if self.double_buttons.__len__() < 37:
            self.add_category_button.show()
            self.add_category_button.raise_()
        else:
            self.add_category_button.hide()

    def selectColor(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.categoryColor.setStyleSheet(get_style_sheet(color.name()))
            self.newColor = color.name()
    
    def edit_category_function(self):
        self.hideUI()
        self.newColor = ''
        self.showSpace.show()
        self.add_category_button.hide()
        self.cancelAddCategory()

        # I don't understand why, but this works to get the text of the category pressed
        self.nameModifiedCategory = self.double_buttons[0].get_first_button_sender_text()

        color = Category.getColorByName(self.nameModifiedCategory)
        self.colorModifiedCategory = color

        self.categoryColor.setStyleSheet(get_style_sheet(color))

        self.categoryNameLabel.show()
        self.categoryColorLabel.show()
        self.saveCategory.show()
        self.categoryColor.show()
        self.categoryName.show()

        self.categoryName.setPlaceholderText(self.nameModifiedCategory)

        self.saveCategory.raise_()
        self.categoryColor.raise_()
        self.categoryName.raise_()

        if self.shortcut:
            window.hideAllButtons()
        else:
            Store.hideAllStores()

    def hideUI(self):
        for button in self.double_buttons:
            button.hide()
        
        self.add_category_button.hide()

        if self.shortcut:
            self.cancelAddCategory()
            window.goHome.show()

    def save_info(self):
        newName = self.categoryName.text().capitalize()

        if newName != "":
            self.reloadNameCategories(newName)

            if UserManager.get_user_role() != 'Offline':
                Mongo.update_category_name(self.nameModifiedCategory, newName)

            self.nameModifiedCategory = newName

        if self.newColor != "":
            self.reloadColorCategories(self.nameModifiedCategory)

            if UserManager.get_user_role() != 'Offline':
                Mongo.update_category_color(self.nameModifiedCategory, self.newColor)

    def reloadNameCategories(self, newName):
        index = Category.getIndexByName(self.nameModifiedCategory)
        Category.changeCategoryName(index, newName)

        update_category_name(window.shortcut_category, self.colorModifiedCategory, self.nameModifiedCategory, newName, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    update_category_name(space, self.colorModifiedCategory, self.nameModifiedCategory, newName)

    def reloadColorCategories(self, newName):
        index = Category.getIndexByName(newName)
        Category.changeCategoryColor(index, self.newColor)

        if window.shortcut_category.name == newName:
            window.shortcut_category.color = self.newColor

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.name == newName:
                        space.category.color = self.newColor

    def showAddCategory(self):
        self.creatingCategory = True

        self.add_category_button.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() + 100)
        self.addCategoryName.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 100)
        self.cancelButtonAddCategory.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 42)
        self.createCategoryButton.move(self.add_category_button.pos().x() + 275, self.add_category_button.pos().y() - 42)
        self.newCategoryColorButton.move(self.add_category_button.pos().x() + 275, self.add_category_button.pos().y() - 100)

        self.add_category_button.setDisabled(True)

        self.addCategoryName.show()
        self.createCategoryButton.show()
        self.newCategoryColorButton.show()
        self.cancelButtonAddCategory.show()

        self.addCategoryName.raise_()
        self.createCategoryButton.raise_()
        self.newCategoryColorButton.raise_()
        self.cancelButtonAddCategory.raise_()

        for button in self.double_buttons:
            button.set_second_button_disabled(True)

    def cancelAddCategory(self):
        self.addCategoryName.hide()
        self.createCategoryButton.hide()
        self.newCategoryColorButton.hide()
        self.cancelButtonAddCategory.hide()

        self.newCategoryName = ""
        self.newCategoryColor = ""

        self.addCategoryName.setText("")
        self.add_category_button.setDisabled(False)
        self.createCategoryButton.setDisabled(True)
        self.newCategoryColorButton.setStyleSheet(get_style_sheet("#FFFFFF"))

        if self.creatingCategory:
            self.add_category_button.move(self.add_category_button.pos().x(), self.add_category_button.pos().y() - 100)
            self.addCategoryName.move(self.addCategoryName.pos().x(), self.addCategoryName.pos().y() - 100)
            self.createCategoryButton.move(self.createCategoryButton.pos().x(), self.createCategoryButton.pos().y() - 100)
            self.newCategoryColorButton.move(self.newCategoryColorButton.pos().x(), self.newCategoryColorButton.pos().y() - 100)
            self.cancelButtonAddCategory.move(self.cancelButtonAddCategory.pos().x(), self.cancelButtonAddCategory.pos().y() - 100)

        for button in self.double_buttons:
            button.set_second_button_disabled(False)

        self.creatingCategory = False

    def selectColorNewCategory(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.newCategoryColorButton.setStyleSheet(get_style_sheet(color.name()))
            self.newCategoryColor = color.name()
        
        if self.newCategoryColor != "" and self.newCategoryName != "":
            self.createCategoryButton.setDisabled(False)

    def changeNewCategoryName(self):
        self.newCategoryName = self.addCategoryName.text()

        if self.newCategoryColor != "" and self.newCategoryName != "":
            self.createCategoryButton.setDisabled(False)

    def createCategory(self):
        Category.add_category(self.newCategoryName.capitalize(), self.newCategoryColor)

        if UserManager.get_user_role() != 'Offline':
            Mongo.add(self.newCategoryName.capitalize(), self.newCategoryColor, False)

        create_category_in(window.shortcut_category, self.newCategoryName.capitalize(), self.mainParent)
        update_category_buttons_pos(window.shortcut_category)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    create_category_in(space.category, self.newCategoryName.capitalize(), self.mainParent)
                    update_category_buttons_pos(space.category)

        self.showUI()
        self.cancelAddCategory()

        posx = self.add_category_button.pos().x()
        posy = self.add_category_button.pos().y()

        if posy + 100 >= WINDOW_HEIGHT:
            posx += 450
            posy = 24
        else:
            posy += 100

        self.add_category_button.move(posx, posy)
        self.addCategoryName.move(posx, posy - 50)
        self.createCategoryButton.move(posx + 100, posy + 50)
        self.newCategoryColorButton.move(posx + 100, posy - 50)
        self.cancelButtonAddCategory.move(posx, posy + 50)
    
    def delete_category_function(self):
        indexButtonPressed = 0
        
        # This time, like we want the index, something that is not inside the button, I made this to know which category is going to be deleted
        for index, send in enumerate(self.double_buttons):
            if send.get_second_button() == self.sender():
                indexButtonPressed = index

        categoryName = Category.getNameByIndex(indexButtonPressed)
        Category.delCategory(indexButtonPressed)

        if UserManager.get_user_role() != 'Offline':
            Mongo.delete_by_name(categoryName)

        delete_category_from(window.shortcut_category, indexButtonPressed, categoryName, True)
        update_category_buttons_pos(window.shortcut_category)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.double_buttons.__len__() > CATEGORY_NAMES.__len__():
                        oldName = space.category.name

                        delete_category_from(space, indexButtonPressed, categoryName)
                        update_category_buttons_pos(space.category)

                        if categoryName == oldName and UserManager.getUserRole() != 'Offline':
                            Mongo.update_category_space(space.mongo_id, space.category.name)

        if self.double_buttons.__len__() <= 1:
            self.double_buttons[0].set_second_button_disabled(True)

class Space(QLabel):
    def __init__(self, posx, posy, actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent = None, long = False, times5Space = 0):
        super().__init__(parent)

        self.setGeometry(posx, posy, 75, 75)

        self.initVariables(actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent, long)
        self.initUI(spaceIndex, parent, times5Space)
        self.initEvents()

    def initVariables(self, actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent, long):
        self.long = long
        self.product = None
        self.mongo_id = None
        self.storeIndex = storeIndex
        self.actualFloor = actualFloor
        self.shelfIndex = shelfIndex
        self.category = SpaceCategory(storeIndex, shelfIndex, spacesInFloorShelf, actualFloor, spaceIndex, parent)
        update_category_buttons_pos(self.category)

        if actualFloor > floors:
            set_unreachable_category(self.category)

    def initUI(self, spaceIndex, parent, times5Space):
        nameSpace = str(times5Space * 5) if times5Space > 0 else ""
        numberSpace = str(spaceIndex + 1)
        
        self.shelfNumber = QLabel(Language.get("shelf") + str(self.shelfIndex + 1), parent)
        self.shelfNumber.setGeometry(int(WINDOW_WIDTH / 2) - int(125 / 2), 25, 125, 25)

        self.box = QPushButton(nameSpace, parent)
        self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 151)

        self.configBox = QPushButton(numberSpace, parent)
        self.configBox.setGeometry(26, 75, 76, 76)

        self.openSpaceConfig = QPushButton(Language.get("go_back"), parent)
        self.openSpaceConfig.setGeometry(1260, 10, 140, 50)
        
        self.labelCategory = QLabel(Language.get("category"), parent)
        self.labelCategory.setGeometry(152, 75, 100, 25)

        self.category_selector = QComboBox(parent)
        self.category_selector.setGeometry(250, 74, 125, 30)
        self.category_selector.addItem(self.category.name)

        self.editCategories = QPushButton("⚙️", parent)

        self.labelCategoryHoldProduct = QLabel(Language.get("category_hold_product"), parent)
        self.labelCategoryHoldProduct.setGeometry(152, 124, 260, 25)
        
        self.category_can_hold_product = InputBool(Language.get('yes'), Language.get('no'), parent, self.categoryCanHoldProduct, self.categoryCanNotHoldProduct)
        self.category_can_hold_product.setGeometry(425, 117, 175, 35)

        if self.long:
            self.box.setFixedHeight(151)
            self.configBox.setFixedHeight(151)
        else:
            self.box.setFixedHeight(76)
            self.configBox.setFixedHeight(76)

        for category in CATEGORY_NAMES:
            if category != self.category.name:
                self.category_selector.addItem(category.capitalize())

        if Category.categoryCanHoldProduct(self.category.name):
            self.category_can_hold_product.set_value(True)

        if UserManager.getUserRole() == 'Offline' or UserManager.getUserRole() == 'Manager':
            self.editCategories.setGeometry(390, 71, 35, 35)
        elif UserManager.getUserRole() == 'Product':
            self.editCategories.setGeometry(0, 0, 0, 0)
        else:
            self.editCategories.setGeometry(0, 0, 0, 0)
            self.category_can_hold_product.set_true_button_disabled(True)
            self.category_can_hold_product.set_false_button_disabled(True)

        self.shelfNumber.setFont(FONT_TEXT)
        
        self.labelCategory.setFont(FONT_SMALL_TEXT)
        self.editCategories.setFont(FONT_SMALL_TEXT)
        self.openSpaceConfig.setFont(FONT_SMALL_TEXT)
        self.category_selector.setFont(FONT_SMALL_TEXT)
        self.labelCategoryHoldProduct.setFont(FONT_SMALL_TEXT)
        
        self.box.setFont(FONT_SMALLEST_CHAR)
        self.configBox.setFont(FONT_SMALLEST_CHAR)

        self.openSpaceConfig.setStyleSheet(DEFAULT_BUTTON)
        self.category_selector.setStyleSheet(COMBO_BOX)
        self.editCategories.setStyleSheet(EDIT_BUTTON)

        self.updateSpaceColor()

    def updateSpaceColor(self):
        self.box.setStyleSheet(get_style_sheet(self.category.color))
        self.configBox.setStyleSheet(get_style_sheet(self.category.color))

    def initEvents(self):
        self.box.clicked.connect(self.configSpace)
        self.openSpaceConfig.clicked.connect(self.stopConfigSpace)
        self.editCategories.clicked.connect(self.openConfigCategories)
        self.category_selector.currentTextChanged.connect(self.changeCategory)
    
    def categoryCanHoldProduct(self):
        Category.changeCategoryCanHoldProduct(self.category_selector.currentText(), True)

        if not isinstance(self.product, Product):
            self.product = Product(153, 165, self, self.parent())
            self.product.show()

            Mongo.update_category_holds_product(self.category_selector.currentText(), True)
            Mongo.update_space_product(self.mongo_id, self.product.select_product.currentText())
            Mongo.update_space_amount(self.mongo_id, 1)
        else:
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.showHideCreateProduct()
    
    def categoryCanNotHoldProduct(self):
        Category.changeCategoryCanHoldProduct(self.category_selector.currentText(), False)

        if isinstance(self.product, Product):
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.showHideCreateProduct()

            self.product.hide()

            self.product = None

            Mongo.update_category_holds_product(self.category_selector.currentText(), False)
            Mongo.update_space_product(self.mongo_id, "")
            Mongo.update_space_amount(self.mongo_id, 0)

    def configSpace(self):
        window.hideAllButtons()

        Store.hideAllStores()
        Store.configSpace(self.storeIndex)

        self.box.hide()

        self.configBox.show()
        self.shelfNumber.show()
        self.labelCategory.show()
        self.editCategories.show()
        self.category_selector.show()
        self.labelCategoryHoldProduct.show()
        self.category_can_hold_product.show()
    
        if isinstance(self.product, Product):
            self.product.show()
        
        window.resizeHeightScroll()
            
    def openConfigCategories(self):
        if isinstance(self.product, Product):
            if self.product.editting_product:
                self.product.show_hide_edit()
            elif self.product.creating_product:
                self.product.showHideCreateProduct()

        Store.configCategory(self.storeIndex)

        window.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

        self.configBox.hide()
        self.shelfNumber.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.category_selector.hide()
        self.labelCategoryHoldProduct.hide()
        self.category_can_hold_product.hide()

        if isinstance(self.product, Product):
            self.product.hide()

        self.openSpaceConfig.show()
        self.category.showUI()

    def stopConfigSpace(self):
        self.updateSpaceColor()

        self.category.cancelAddCategory()

        ShelfInfo.hideAllSpaces()

        Store.stopConfigCategory(self.storeIndex)

        self.configBox.show()
        self.shelfNumber.show()
        self.labelCategory.show()
        self.editCategories.show()
        self.category_selector.show()
        self.labelCategoryHoldProduct.show()
        self.category_can_hold_product.show()

        if isinstance(self.product, Product):
            self.product.show()

        self.openSpaceConfig.hide()
    
    def changeCategory(self, category):
        oldName = self.category.name

        set_category_by_name(self.category, category)
        self.updateSpaceColor()

        if Category.categoryCanHoldProduct(category):
            self.category_can_hold_product.set_value(True)

            if not isinstance(self.product, Product):
                self.product = Product(153, 165, self, self.parent())
                self.product.show()

                Mongo.update_space_product(self.mongo_id, self.product.select_product.currentText())
                Mongo.update_space_amount(self.mongo_id, 1)

        else:
            self.category_can_hold_product.set_value(False)

            if isinstance(self.product, Product):
                self.product.hide()

            self.product = None

        if UserManager.getUserRole() != 'Offline':
            Mongo.update_category_space(self.mongo_id, oldName)

    def updateVerticalHeaderPosition(self, value):
        self.openSpaceConfig.move(self.openSpaceConfig.pos().x(), value + 15)

    def showFloor(self, number):
        if number != self.actualFloor:
            self.hideSpace()
        else:
            self.showSpace()

    def hideSpace(self):
        self.box.hide()
        self.configBox.hide()
        self.shelfNumber.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category_selector.hide()
        self.labelCategoryHoldProduct.hide()
        self.category_can_hold_product.hide()

        if isinstance(self.product, Product):
            self.product.hide()
        
        self.category.hideUI()

    def showSpace(self):
        self.updateSpaceColor()

        self.box.show()

        self.configBox.hide()
        self.shelfNumber.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category_selector.hide()
        self.labelCategoryHoldProduct.hide()
        self.category_can_hold_product.hide()

        if isinstance(self.product, Product):
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
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, False, times5))

                    indexSpace += 1

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (75 * index), posy + 75, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent))
                    indexSpace += 1
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (75 * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, True, times5))

                    indexSpace += 1
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, index, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (75 * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, index, parent, False, times5))

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

        for i in SHELVES_FORMS:
            spacesInfo = []

            time.sleep(0.01)

            for floor in range(storeFloors):
                for _ in range(i.spaces):
                    id_category = id_unreachable_category if i.floors - 1 < floor else id_empty_category 

                    spacesInfo.append({
                        "category": id_category,
                        "mongo_id": name + "_" + str(mongo_id),
                        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    })

                    mongo_id += 1
            
            shelvesInfo.append({
                "floors": i.floors,
                "spaces": spacesInfo,
                "double_shelf": i.double_shelf,
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

        for index, i in enumerate(SHELVES_FORMS):
            storeShelves.append(ShelfInfo(25, 50 + (225 * index), i.floors, i.spaces, i.double_shelf, self.floor, (index + 1), STORES.__len__(), parent))
        
        SHELVES.append(storeShelves)
        SHELVES_FORMS.clear()
        
        Shelf.createShelf(parent)
        Shelf.hideAllForms()

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
        window.resizeHeightScroll(amountShelves * 225 - 100)
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

class Shelf(QLabel):
    @staticmethod
    def createShelf(parent):
        length = SHELVES_FORMS.__len__()

        if length > 0:
            newShelf = Shelf(Language.get("shelf") + str(length + 1), SHELVES_FORMS[length - 1].pos().x(), SHELVES_FORMS[length - 1].pos().y() + 200, parent)
        else:
            newShelf = Shelf(Language.get("shelf") + str(length + 1), 400, 300, parent)
        
        newShelf.showForm()

        SHELVES_FORMS.append(newShelf)

    @staticmethod
    def hideAllForms():
        for shelf in SHELVES_FORMS:
            shelf.hideForm()

    @staticmethod
    def showAllForms():    
        for shelf in SHELVES_FORMS:
            shelf.showForm()

    def __init__(self, name, posx, posy, parent = None):
        super().__init__(parent)
        
        self.setGeometry(posx, posy, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.initVariables()
        self.initUI(name)
        self.hideForm()
    
    def initVariables(self):
        self.double_shelf = False
        self.spaces = 1
        self.floors = 1

    def initUI(self, name):
        # Config shelf
        self.shelf_label = QLabel(name, self) # shelfLabel
        self.shelf_label.setGeometry(0, 10, 150, 35)

        self.inputSpacesLabel = QLabel(Language.get("shelf_question_1"), self)
        self.inputSpacesLabel.setGeometry(0, 55, 500, 35)

        self.input_spaces = InputInteger(1, True, self)
        self.input_spaces.setGeometry(480, 35, 175, 65)

        self.doubleShelfLabel = QLabel(Language.get("shelf_question_2"), self)
        self.doubleShelfLabel.setGeometry(0, 95, 500, 35)

        self.double_shelf_input = InputBool(Language.get("yes"), Language.get("no"), self)
        self.double_shelf_input.setGeometry(480, 92, 175, 34)

        self.shelfFloorsLabel = QLabel(Language.get("shelf_question_4"), self)
        self.shelfFloorsLabel.setGeometry(0, 135, 500, 35)

        self.input_shelf_floors = InputInteger(1, True, self)
        self.input_shelf_floors.setGeometry(480, 123, 175, 65)

        # Option to delete shelf if there is more than one shelf
        if SHELVES_FORMS.__len__() + 1 > 1:
            self.delShelfButton = QPushButton("❌", self)
            self.delShelfButton.setFont(FONT_SMALLEST_CHAR)
            self.delShelfButton.setGeometry(150, 15, 50, 25)
            self.delShelfButton.setStyleSheet(REST_BUTTON)

            self.delShelfButton.clicked.connect(self.delShelf)

            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 650, 3)
            self.separator.setStyleSheet(BACKGROUND_BLACK)

        # Style
        self.shelf_label.setFont(FONT_TEXT)

        self.inputSpacesLabel.setFont(FONT_SMALL_TEXT)
        self.doubleShelfLabel.setFont(FONT_SMALL_TEXT)
        self.shelfFloorsLabel.setFont(FONT_SMALL_TEXT)

    def hideForm(self):
        self.hide()

    def delShelf(self):
        shelfToDelete = 0
        
        for index, shelf in enumerate(SHELVES_FORMS):
            try:
                if self.sender() == shelf.delShelfButton:
                    shelfToDelete = index
                    break
            except AttributeError:
                continue
        
        SHELVES_FORMS[shelfToDelete].hide()
        del SHELVES_FORMS[shelfToDelete]

        update_shelves_pos(SHELVES_FORMS)
        window.resizeHeightScroll()

    def showForm(self):
        self.show()

    def saveInfo(self):
        self.spaces = self.input_spaces.get_value()
        self.floors = self.input_shelf_floors.get_value()
        self.double_shelf = self.double_shelf_input.get_value()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initVariables()
        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeHeightScroll()

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

        self.shortcut_category = SpaceCategory(0, 0, 0, 0, 0, self.widget, True)

    def initUI(self, parent):
        # Main buttons
        self.goHome = QPushButton(Language.get("go_back"), parent)
        self.goHome.setGeometry(1260, 10, 140, 50)
        self.goHome.hide()

        self.addStoreButton = QPushButton(Language.get("add_store"), parent)
        self.editCategories = QPushButton(Language.get("edit_categories"), parent)

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
        self.editCategories.setFont(FONT_SMALL_TEXT)
        self.store_name_input.setFont(FONT_SMALL_TEXT)

        self.goHome.setStyleSheet(DEFAULT_BUTTON)
        self.store_name_input.setStyleSheet(INPUT_TEXT)
        self.addStoreButton.setStyleSheet(BLUE_BUTTON)
        self.editCategories.setStyleSheet(EDIT_BUTTON)
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
        self.editCategories.clicked.connect(self.configCategories)
        self.icon_new_store.clicked.connect(self.uploadImage)
        self.setDefaultIcon.clicked.connect(self.setDefaultStoreIcon)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)
    
    # Scroll functions
    def updateVerticalHeaderPosition(self, value):
        self.goHome.move(self.goHome.pos().x(), value + 10)
        self.editCategories.move(self.editCategories.pos().x(), value + (WINDOW_HEIGHT - 115))
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
    def resizeHeightScroll(self, height = 0):
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
        self.shortcut_category.hideUI()

        self.showMainButtons()
        self.hideAddStoreForm()
        self.raiseMainButtons()

        Shelf.hideAllForms()
        Store.hideAllStores()
        Store.showAllStoreIcons()
        ShelfInfo.hideAllSpaces()

        self.raiseMainButtons()
        self.resizeMain()

    def addStore(self):
        self.showAddStoreForm()
        self.resizeHeightScroll()
        
        if SHELVES_FORMS.__len__() == 0:
            self.createShelf()

        Shelf.showAllForms()
        Store.hideAllStoreIcons()

        self.goHome.show()
        self.goHome.raise_()
        self.addStoreButton.hide()
        self.editCategories.hide()
        self.languageChanger.hide()

    def createShelf(self):
        Shelf.createShelf(self.widget)
    
        self.resizeHeightScroll()

    def saveStoreInfo(self):
        save_shelves_info(SHELVES_FORMS)

        storeName = self.store_name_input.text().strip()

        if storeName.__len__() <= 15:
            if storeName == "":
                storeName = Language.get("store") + str(STORES.__len__() + 1)

            if UserManager.getUserRole() != 'Offline':
                Store.createMongoStore(storeName, self.image)

            Shelf.hideAllForms()
            Store.createStore(storeName, self.widget, self.image)

            self.store_name_input.setText("")
            self.store_name_input.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))

            self.re_open_home()
            self.goHome.raise_()
        else:
            QMessageBox.warning(None, "Name too long", "The store name must be maximum 15 digits long")
    
    def configCategories(self):
        Store.hideAllStoreIcons()

        self.shortcut_category.showUI()

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
        self.editCategories.show()
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
        self.editCategories.hide()
        self.languageChanger.hide()

    # Hide and show objects
    def hideMainButtons(self):
        self.goHome.show()
        self.addStoreButton.hide()
        self.editCategories.hide()
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
        self.editCategories.raise_()

    def change_user_role(self, role, username = ''):
        if role != 'Offline':
            UserManager.setUser(username, role)

        if UserManager.getUserRole() == 'Offline' or UserManager.getUserRole() == 'Manager':
            self.addStoreButton.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 75, 190, 50)
            self.editCategories.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 115, 190, 30)
        else:
            self.addStoreButton.setGeometry(0, 0, 0, 0)
            self.editCategories.setGeometry(0, 0, 0, 0)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if UserManager.getUserRole() == 'Offline' or UserManager.getUserRole() == 'Manager':
                        space.editCategories.setGeometry(320, 26, 26, 26)
                    else:
                        space.editCategories.setGeometry(0, 0, 0, 0)

window = MainWindow()

class main():
    logInWindow = LogInWindow(window)
    logInWindow.show()

    sys.exit(app.exec_())

    Mongo.close_connection()

if __name__ == "__main__":
    main()
