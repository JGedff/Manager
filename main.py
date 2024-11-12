import os
import sys
import time
import shutil
from datetime import datetime

from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QColorDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel, QPushButton

from utils.functions.shelfFunctions import updateShelfPosition

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS, STORES, DEFAULT_IMAGE, SHELVES, DEFAULT_SPACE_MARGIN, CATEGORY_NAMES, FONT_TITLE, FONT_BIG_TEXT, FONT_TEXT, FONT_SMALL_TEXT, FONT_SMALLEST_CHAR

from utils.functions.globalFunctions import getMaxFloor
from utils.functions.shelfFunctions import saveShelfInfo, updateShelfPosition
from utils.functions.spaceCategoryFunctions import setUnreachableCategory, setCategoryByName, createCategoryIn, updateNameCategory, deleteCategoryFrom, updateButtonsPosition, setEmptyCategory, getEmptyCategoryName, getUnreachableCategoryName

from utils.mongoDb import Mongo
from utils.userManager import UserManager

from utils.language import Language
from utils.category import Category
from utils.inputBool import InputBool
from utils.inputNumber import InputNumber
from utils.imageButton import ImageButton
from utils.doubleButton import DoubleButton

from components.languageChanger import LanguageChanger

app = QApplication(sys.argv)

class SpaceCategory(QLabel):
    def __init__(self, storeIndex = 0, shelfIndex = 0, spacesInFloorShelf = 0, floor = 0, spaceIndex = 0, parent = None, shortcut = False):
        super().__init__(parent)

        self.initVariables(storeIndex, shelfIndex, spacesInFloorShelf, floor, spaceIndex, parent, shortcut)
        self.initUI(parent)
        self.initEvents()

        setEmptyCategory(self)

    def initVariables(self, storeIndex, shelfIndex, spacesInFloorShelf, floor, spaceIndex, parent, shortcut):
        self.name = ''
        self.color = ''
        self.newColor = ''
        self.floor = floor
        self.doubleButtons = []
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
        self.showSpace.setGeometry(1300, 15, 100, 50)
        self.showSpace.hide()

        self.categoryNameLabel = QLabel(Language.get("category_name"), parent)
        self.categoryNameLabel.setGeometry(25, 25, 125, 25)
        self.categoryNameLabel.hide()

        self.categoryName = QLineEdit(parent)
        self.categoryName.setGeometry(175, 25, 125, 25)
        self.categoryName.hide()
        
        self.categoryColorLabel = QLabel(Language.get("category_color"), parent)
        self.categoryColorLabel.setGeometry(25, 75, 125, 25)
        self.categoryColorLabel.hide()

        self.categoryColor = QPushButton(Language.get("select_color"), parent)
        self.categoryColor.setGeometry(175, 75, 125, 25)
        self.categoryColor.hide()

        self.saveCategory = QPushButton(Language.get("save"), parent)
        self.saveCategory.setGeometry(175, 125, 125, 25)
        self.saveCategory.hide()

        posx = 25
        posy = 25

        for category in CATEGORY_NAMES:
            newDoubleButton = DoubleButton(posx, posy, category.capitalize(), "🗑️", self.editCategory, self.deleteCategory, parent)
            posy += 50

            self.doubleButtons.append(newDoubleButton)

        self.addCategory = QPushButton(Language.get("add_category"), parent)
        self.addCategory.setGeometry(posx, posy, 200, 25)
        self.addCategory.hide()

        self.addCategoryName = QLineEdit(parent)
        self.addCategoryName.setGeometry(posx, posy - 100, 200, 25)
        self.addCategoryName.setPlaceholderText(Language.get("name"))
        self.addCategoryName.hide()

        self.newCategoryColorButton = QPushButton(Language.get("select_color"), parent)
        self.newCategoryColorButton.setGeometry(posx + 225, posy - 50, 125, 25)
        self.newCategoryColorButton.hide()

        self.cancelButtonAddCategory = QPushButton(Language.get("cancel"), parent)
        self.cancelButtonAddCategory.setGeometry(posx, posy - 50, 100, 25)
        self.cancelButtonAddCategory.hide()

        self.createCategoryButton = QPushButton(Language.get("create"), parent)
        self.createCategoryButton.setGeometry(posx + 425, posy - 50, 100, 25)
        self.createCategoryButton.setDisabled(True)
        self.createCategoryButton.hide()

    def initEvents(self):
        self.showSpace.clicked.connect(self.stopEditCategory)
        self.categoryColor.clicked.connect(self.selectColor)
        self.saveCategory.clicked.connect(self.saveInfo)
        self.addCategory.clicked.connect(self.showAddCategory)
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
        for button in self.doubleButtons:
            button.show()
            button.raise_()

        self.addCategory.show()
        self.addCategory.raise_()

    def selectColor(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.categoryColor.setStyleSheet("background-color: " + color.name())
            self.newColor = color.name()
    
    def editCategory(self):
        self.hideUI()
        self.newColor = ''
        self.showSpace.show()
        self.cancelAddCategory()
            
        # self.doubleButtons[0].button1.sender() will be used as the receptor of events
        self.nameModifiedCategory = self.doubleButtons[0].button1.sender().text()
        color = Category.getColorByName(self.nameModifiedCategory)
        self.colorModifiedCategory = color

        self.categoryColor.setStyleSheet("background-color: " + color)

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
        for button in self.doubleButtons:
            button.hide()
        
        self.addCategory.hide()

        if self.shortcut:
            window.goHome.show()

    
    def saveInfo(self):
        newName = self.categoryName.text().capitalize()

        if newName != "":
            self.reloadNameCategories(newName)

            if window.userRole == 'Admin':
                Mongo.updateMongoCategoryName(self.nameModifiedCategory, newName)

            self.nameModifiedCategory = newName

        if self.newColor != "":
            self.reloadColorCategories(self.nameModifiedCategory)

            if window.userRole == 'Admin':
                Mongo.updateMongoCategoryColor(self.nameModifiedCategory, self.newColor)

    def reloadNameCategories(self, newName):
        index = Category.getIndexByName(self.nameModifiedCategory)
        Category.changeCategoryName(index, newName)

        updateNameCategory(window.categoryManager, self.colorModifiedCategory, self.nameModifiedCategory, newName, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    updateNameCategory(space, self.colorModifiedCategory, self.nameModifiedCategory, newName)

    def reloadColorCategories(self, newName):
        index = Category.getIndexByName(newName)
        Category.changeCategoryColor(index, self.newColor)

        if window.categoryManager.name == newName:
            window.categoryManager.color = self.newColor

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.name == newName:
                        space.category.color = self.newColor

    def showAddCategory(self):
        self.creatingCategory = True

        self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 100)
        self.addCategoryName.move(self.addCategory.pos().x(), self.addCategory.pos().y() - 100)
        self.createCategoryButton.move(self.addCategory.pos().x() + 400, self.addCategory.pos().y() - 50)
        self.newCategoryColorButton.move(self.addCategory.pos().x() + 225, self.addCategory.pos().y() - 50)
        self.cancelButtonAddCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() - 50)

        self.addCategory.setDisabled(True)

        self.addCategoryName.show()
        self.createCategoryButton.show()
        self.newCategoryColorButton.show()
        self.cancelButtonAddCategory.show()

        self.addCategoryName.raise_()
        self.createCategoryButton.raise_()
        self.newCategoryColorButton.raise_()
        self.cancelButtonAddCategory.raise_()

        for button in self.doubleButtons:
            button.setDisabledButton2(True)

    def cancelAddCategory(self):
        self.addCategoryName.hide()
        self.createCategoryButton.hide()
        self.newCategoryColorButton.hide()
        self.cancelButtonAddCategory.hide()

        self.newCategoryName = ""
        self.newCategoryColor = ""

        self.addCategoryName.setText("")
        self.addCategory.setDisabled(False)
        self.createCategoryButton.setDisabled(True)
        self.newCategoryColorButton.setStyleSheet("background-color: white")

        if self.creatingCategory:
            self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() - 100)
            self.addCategoryName.move(self.addCategoryName.pos().x(), self.addCategoryName.pos().y() - 100)
            self.createCategoryButton.move(self.createCategoryButton.pos().x(), self.createCategoryButton.pos().y() - 100)
            self.newCategoryColorButton.move(self.newCategoryColorButton.pos().x(), self.newCategoryColorButton.pos().y() - 100)
            self.cancelButtonAddCategory.move(self.cancelButtonAddCategory.pos().x(), self.cancelButtonAddCategory.pos().y() - 100)

        for button in self.doubleButtons:
            button.setDisabledButton2(False)

        self.creatingCategory = False

    def selectColorNewCategory(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.newCategoryColorButton.setStyleSheet("background-color: " + color.name())
            self.newCategoryColor = color.name()
        
        if self.newCategoryColor != "" and self.newCategoryName != "":
            self.createCategoryButton.setDisabled(False)

    def changeNewCategoryName(self):
        self.newCategoryName = self.addCategoryName.text()

        if self.newCategoryColor != "" and self.newCategoryName != "":
            self.createCategoryButton.setDisabled(False)

    def createCategory(self):
        Category.addCategory(self.newCategoryName.capitalize(), self.newCategoryColor)

        if window.userRole == 'Admin':
            Mongo.addMongoCategory(self.newCategoryName.capitalize(), self.newCategoryColor)

        createCategoryIn(window.categoryManager, self.newCategoryName.capitalize(), self.mainParent, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    createCategoryIn(space, self.newCategoryName.capitalize(), self.mainParent)
        
        self.showUI()
        self.cancelAddCategory()

        self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 100)
        self.addCategoryName.move(self.addCategoryName.pos().x(), self.addCategoryName.pos().y() + 50)
        self.createCategoryButton.move(self.createCategoryButton.pos().x(), self.createCategoryButton.pos().y() + 50)
        self.newCategoryColorButton.move(self.newCategoryColorButton.pos().x(), self.newCategoryColorButton.pos().y() + 50)
        self.cancelButtonAddCategory.move(self.cancelButtonAddCategory.pos().x(), self.cancelButtonAddCategory.pos().y() + 50)
    
    def deleteCategory(self):
        indexButtonPressed = 0
        
        for index, send in enumerate(self.doubleButtons):
            if send.button2 == self.sender():
                indexButtonPressed = index

        categoryName = Category.getNameByIndex(indexButtonPressed)
        Category.delCategory(indexButtonPressed)

        if window.userRole == 'Admin':
            Mongo.delMongoCategory(categoryName)

        deleteCategoryFrom(window.categoryManager, indexButtonPressed, categoryName, True)
        updateButtonsPosition(window.categoryManager, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.doubleButtons.__len__() > CATEGORY_NAMES.__len__():
                        oldName = space.category.name

                        deleteCategoryFrom(space, indexButtonPressed, categoryName)
                        updateButtonsPosition(space)

                        if categoryName == oldName and window.userRole == 'Admin':
                            Mongo.updateMongoSpaceCategory(space.mongo_id, space.category.name)

        if self.doubleButtons.__len__() <= 1:
            self.doubleButtons[0].setDisabledButton2(True)

class Space(QLabel):
    def __init__(self, posx, posy, actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent = None, long = False, times5Space = 0):
        super().__init__(parent)

        self.setGeometry(posx, posy, 75, 75)

        self.initVariables(actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent, long)
        self.initUI(parent, times5Space)
        self.initEvents()
        
    def initVariables(self, actualFloor, floors, storeIndex, shelfIndex, spacesInFloorShelf, spaceIndex, parent, long):
        self.mongo_id = None
        self.long = long
        self.storeIndex = storeIndex
        self.actualFloor = actualFloor
        self.category = SpaceCategory(storeIndex, shelfIndex, spacesInFloorShelf, actualFloor, spaceIndex, parent)

        if actualFloor > floors:
            setUnreachableCategory(self.category)

    def initUI(self, parent, times5Space):
        nameSpace = str(times5Space * 5) if times5Space > 0 else ""
        
        self.box = QPushButton(nameSpace, parent)

        if self.long:
            self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 151)
        else:
            self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 76)

        self.openSpaceConfig = QPushButton(Language.get("go_back"), parent)
        self.openSpaceConfig.setGeometry(1300, 15, 100, 50)
        
        self.configBox = QPushButton(parent)
        self.configBox.setGeometry(26, 26, 76, 76)

        self.labelCategory = QLabel(Language.get("category"), parent)
        self.labelCategory.setGeometry(152, 26, 50, 25)

        self.categorySelector = QComboBox(parent)
        self.categorySelector.setGeometry(210, 26, 100, 25)
        self.categorySelector.addItem(self.category.name)

        for category in CATEGORY_NAMES:
            if category != self.category.name:
                self.categorySelector.addItem(category.capitalize())

        self.editCategories = QPushButton("⚙️", parent)

        if window.userRole == 'Offline' or window.userRole == 'Admin':
            self.editCategories.setGeometry(320, 26, 26, 26)
        else:
            self.editCategories.setGeometry(0, 0, 0, 0)

        self.updateSpaceColor()

    def updateSpaceColor(self):
        self.box.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")
        self.configBox.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")

    def initEvents(self):
        self.box.clicked.connect(self.configSpace)
        self.openSpaceConfig.clicked.connect(self.stopConfigSpace)
        self.editCategories.clicked.connect(self.openConfigCategories)
        self.categorySelector.currentTextChanged.connect(self.changeCategory)

    def configSpace(self):
        window.hideAllButtons()

        Store.hideAllStores()
        Store.configSpace(self.storeIndex)

        self.configBox.show()
        self.labelCategory.show()
        self.categorySelector.show()
        self.editCategories.show()
        self.updateScrollToDefault()
            
    def openConfigCategories(self):
        Store.configCategory(self.storeIndex)

        self.updateScroll()

        self.configBox.hide()
        self.labelCategory.hide()
        self.categorySelector.hide()
        self.editCategories.hide()

        self.openSpaceConfig.show()
        self.category.showUI()
    
    def updateScroll(self):
        if self.category.doubleButtons[self.category.doubleButtons.__len__() - 1].pos().y() >= 500:
            window.resizeHeightScroll(self.category.doubleButtons[self.category.doubleButtons.__len__() - 1].pos().y() + 200)
        else:
            self.updateScrollToDefault()

    def stopConfigSpace(self):
        self.updateScrollToDefault()
        self.updateSpaceColor()

        self.category.cancelAddCategory()

        ShelfInfo.hideAllSpaces()
        Store.stopConfigCategory(self.storeIndex)

        self.configBox.show()
        self.configBox.show()
        self.labelCategory.show()
        self.editCategories.show()
        self.categorySelector.show()
    
    def changeCategory(self, category):
        oldName = self.category.name

        setCategoryByName(self.category, category)
        self.updateSpaceColor()

        if window.userRole == 'Admin':
            Mongo.updateMongoSpaceCategory(self.mongo_id, category, oldName)

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
        self.categorySelector.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category.hideUI()

    def showSpace(self):
        self.updateSpaceColor()

        self.box.show()

        self.configBox.hide()
        self.categorySelector.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()

        self.box.raise_()

    def updateScrollToDefault(self):
        window.resizeHeightScroll()

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
        self.shelfNumber.setGeometry(int(WINDOW_WIDTH / 2 - self.shelfNumber.width() / 2), posy - 25, 100, 25)
        self.shelfNumber.hide()

        for actualFloor in range(self.storeFloors):
            times5 = 0

            if self.double_shelf:
                indexSpace = 0
                mod = self.spacesLength % 2
                sideSpaces = (self.spacesLength / 2).__trunc__()

                for index in range(sideSpaces):
                    if (index + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, False, times5))

                    indexSpace += 1

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy + DEFAULT_SPACE_MARGIN, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent))
                    indexSpace += 1
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, indexSpace, parent, True, times5))

                    indexSpace += 1
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, index, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, self.spacesLength, index, parent, False, times5))

    def initEvents(self):
        updateShelfPosition()
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

        storeFloors = getMaxFloor()
        emptyCategory = getEmptyCategoryName()
        unreachableCategory = getEmptyCategoryName()
        id_empty_category = Mongo.getMongoCategoryByName(emptyCategory, emptyCategory)
        id_unreachable_category = Mongo.getMongoCategoryByName(unreachableCategory, unreachableCategory)

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
            
        Mongo.addStoreToMongo(shelvesInfo, name, image_path)
        
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
            store.hideIcon()

    @staticmethod
    def showAllStoreIcons():
        for store in STORES:
            store.showIcon()

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
        self.floor = getMaxFloor()
        storeShelves = []

        for index, i in enumerate(SHELVES_FORMS):
            storeShelves.append(ShelfInfo(25, 50 + (185 * index), i.floors, i.spaces, i.double_shelf, self.floor, (index + 1), STORES.__len__(), parent))
        
        SHELVES.append(storeShelves)
        SHELVES_FORMS.clear()
        
        Shelf.createShelf(parent)
        Shelf.hideAllForms()

    def initUI(self, name, image, posx, posy, parent):
        self.goBackStore = QPushButton(Language.get("go_back"), parent)
        self.goBackStore.setGeometry(1300, 15, 100, 50)

        self.storeIcon = ImageButton(name, image, parent)
        self.storeIcon.setGeometry(posx, posy, 150, 150)

        self.changeFloorButton = QComboBox(parent)
        self.changeFloorButton.setGeometry(25, 15, 125, 25)

        for index in range(self.floor):
            self.changeFloorButton.addItem(Language.get("floor") + str(index + 1))

    def initEvents(self):
        self.storeIcon.clicked.connect(self.openStore)
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
        window.resizeHeightScroll(amountShelves * 185 - 100)
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

    def showIcon(self):
        self.storeIcon.show()

    def hideIcon(self):
        self.storeIcon.hide()

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
        for i in SHELVES_FORMS:
            i.showForm()

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
        self.shelfLabel = QLabel(name, self)
        self.shelfLabel.setGeometry(0, 10, 150, 35)

        self.inputSpacesLabel = QLabel(Language.get("shelf_question_1"), self)
        self.inputSpacesLabel.setGeometry(0, 55, 500, 35)

        self.inputSpaces = InputNumber(1, True, self)
        self.inputSpaces.setGeometry(480, 35, 175, 65)

        self.doubleShelfLabel = QLabel(Language.get("shelf_question_2"), self)
        self.doubleShelfLabel.setGeometry(0, 95, 500, 35)

        self.doubleShelfInput = InputBool(Language.get("yes"), Language.get("no"), self)
        self.doubleShelfInput.setGeometry(480, 80, 175, 65)

        self.shelfFloorsLabel = QLabel(Language.get("shelf_question_4"), self)
        self.shelfFloorsLabel.setGeometry(0, 135, 500, 35)

        self.shelfFloorsInput = InputNumber(1, True, self)
        self.shelfFloorsInput.setGeometry(480, 123, 175, 65)

        # Option to delete shelf if there is more than one shelf
        if SHELVES_FORMS.__len__() + 1 > 1:
            self.delShelfButton = QPushButton("❌", self)
            self.delShelfButton.setFont(FONT_SMALLEST_CHAR)
            self.delShelfButton.setGeometry(150, 15, 50, 25)
            self.delShelfButton.setStyleSheet("background-color: #FFD1D1; border: 1px solid #AFAFAF")

            self.delShelfButton.clicked.connect(self.delShelf)

            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 650, 3)
            self.separator.setStyleSheet("background-color: black")

        # Style
        self.shelfLabel.setFont(FONT_TEXT)

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

        updateShelfPosition()
        window.resizeHeightScroll()

    def showForm(self):
        self.show()

    def saveInfo(self):
        self.spaces = self.inputSpaces.getNum()
        self.floors = self.shelfFloorsInput.getNum()
        self.double_shelf = self.doubleShelfInput.getValue()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initVariables()
        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeHeightScroll()

    def initVariables(self):
        self.userRole = 'Guest'
        self.image = DEFAULT_IMAGE

        # Window config
        self.setWindowTitle(Language.get("window_title"))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add scroll to window
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

        self.categoryManager = SpaceCategory(0, 0, 0, 0, 0, self.widget, True)

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
        self.headerFormBackground.setStyleSheet("background-color: #dddddd;")
        self.headerFormBackground.hide()

        self.storeNameLabel = QLabel(Language.get("name_store"), parent)
        self.storeNameLabel.setGeometry(400, 20, 200, 35)
        self.storeNameLabel.hide()
        
        self.storeNameInput = QLineEdit(parent)
        self.storeNameInput.setGeometry(690, 10, 355, 50)
        self.storeNameInput.setPlaceholderText(Language.get("store") + str(1))
        self.storeNameInput.hide()

        # Body form
        self.formStoreIcon = ImageButton(Language.get("change_image"), DEFAULT_IMAGE, parent)
        self.formStoreIcon.setGeometry(int(WINDOW_WIDTH / 2) - 75, 115, 150, 150)
        self.formStoreIcon.hide()

        # Footer form
        self.footerFormBackground = QLabel("", parent)
        self.footerFormBackground.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.footerFormBackground.setStyleSheet("background-color: #dddddd;")
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
        self.storeNameInput.setFont(FONT_SMALL_TEXT)

        self.goHome.setStyleSheet("background-color: white; border: 1px solid #CACACA")
        self.storeNameInput.setStyleSheet("border: 1px solid #CACACA; padding-left: 5px")
        self.addStoreButton.setStyleSheet("background-color: #A4F9FF; border: 1px solid #88C6CB")
        self.editCategories.setStyleSheet("background-color: #FFE397; border: 1px solid #CDB87D")
        self.addShelfButton.setStyleSheet("background-color: #A4F9FF; border: 1px solid #88C6CB")
        self.createStoreButton.setStyleSheet("background-color: #59CC4E; color: white; border: 0px")

        Store.showAllStoreIcons()

    def initEvents(self):
        # Click buttons
        self.goHome.clicked.connect(self.reOpenHome)
        self.addStoreButton.clicked.connect(self.addStore)
        self.addShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.saveStoreInfo)
        self.editCategories.clicked.connect(self.configCategories)
        self.formStoreIcon.clicked.connect(self.uploadImage)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)
    
    # Scroll functions
    def updateVerticalHeaderPosition(self, value):
        self.goHome.move(self.goHome.pos().x(), value + 10)
        self.editCategories.move(self.editCategories.pos().x(), value + (WINDOW_HEIGHT - 115))
        self.storeNameInput.move(self.storeNameInput.pos().x(), value + 10)
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
            self.widget.resize(WINDOW_WIDTH - 20, STORES[STORES.__len__() - 1].storeIcon.pos().y() + 290)

    # UI functions
    def reOpenHome(self):
        self.categoryManager.hideUI()

        self.showMainButtons()
        self.hideAddStoreForm()
        self.raiseMainButtons()

        Shelf.hideAllForms()
        Store.hideAllStores()
        Store.showAllStoreIcons()
        ShelfInfo.hideAllSpaces()

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
        self.editCategories.hide()

    def createShelf(self):
        Shelf.createShelf(self.widget)
    
        self.resizeHeightScroll()

    def saveStoreInfo(self):
        saveShelfInfo()

        storeName = self.storeNameInput.text().strip()

        if storeName.__len__() <= 15:
            if storeName == "":
                storeName = Language.get("store") + str(STORES.__len__() + 1)

            if window.userRole == 'Admin':
                Store.createMongoStore(storeName, self.image)

            Shelf.hideAllForms()
            Store.createStore(storeName, self.widget, self.image)

            self.storeNameInput.setText("")
            self.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))

            self.reOpenHome()
            self.goHome.raise_()
        else:
            QMessageBox.warning(None, "Name too long", "The store name must be maximum 15 digits long")
    
    def configCategories(self):
        Store.hideAllStoreIcons()

        self.categoryManager.showUI()

        self.hideMainButtons()

    def uploadImage(self):
        # Open a file dialog to select an image file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        
        # Check if a file was selected
        if file_path:
            self.image = file_path
            self.formStoreIcon.setPixmap(file_path)

    # Show objects
    def showAddStoreForm(self):
        self.headerFormBackground.show()
        self.footerFormBackground.show()
        self.createStoreButton.show()
        self.storeNameInput.show()
        self.storeNameLabel.show()
        self.addShelfButton.show()
        self.formStoreIcon.show()

    def showMainButtons(self):
        self.languageChanger.show()
        self.editCategories.show()
        self.addStoreButton.show()

    # Hide objects
    def hideAddStoreForm(self):
        self.headerFormBackground.hide()
        self.footerFormBackground.hide()
        self.createStoreButton.hide()
        self.storeNameInput.hide()
        self.storeNameLabel.hide()
        self.addShelfButton.hide()
        self.formStoreIcon.hide()
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
        self.storeNameInput.raise_()
        self.storeNameLabel.raise_()
        self.goHome.raise_()
    
    def raiseMainButtons(self):
        self.languageChanger.raise_()
        self.addStoreButton.raise_()
        self.editCategories.raise_()

    def changeUserRole(self, role):
        self.userRole = role

        if self.userRole == 'Offline' or self.userRole == 'Admin':
            self.addStoreButton.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 75, 190, 50)
            self.editCategories.setGeometry(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 115, 190, 30)
        else:
            self.addStoreButton.setGeometry(0, 0, 0, 0)
            self.editCategories.setGeometry(0, 0, 0, 0)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if window.userRole == 'Offline' or window.userRole == 'Admin':
                        space.editCategories.setGeometry(320, 26, 26, 26)
                    else:
                        space.editCategories.setGeometry(0, 0, 0, 0)

class LogInWindow(QMainWindow):
    def __init__(self, mainApp):
        super().__init__()

        self.initVariables(mainApp)
        self.initUI(self.widget)
        self.initEvents()

        self.setCentralWidget(self.scroll)

    def initVariables(self, mainApp):
        self.logged = ""
        self.logIn = True
        self.mainApp = mainApp

        self.setWindowTitle(Language.get("log_in"))
        self.setFixedSize(395, 605)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(390, 600)
        self.scroll.setWidget(self.widget)
    
    def initUI(self, parent):
        self.languageChanger = LanguageChanger(self, parent)
        self.languageChanger.setGeometry(265, 15, 100, 30)

        self.logInTitle = QLabel(Language.get("log_in"), parent)
        self.logInTitle.setGeometry(85, 55, 225, 50)
        
        self.registerTitle = QLabel(Language.get("register"), parent)
        self.registerTitle.setGeometry(85, 55, 225, 50)
        self.registerTitle.hide()

        self.userLabel = QLabel(Language.get("user_name"), parent)
        self.userLabel.setGeometry(15, 120, 200, 25)

        self.passwordLabel = QLabel(Language.get("password"), parent)
        self.passwordLabel.setGeometry(15, 220, 200, 25)

        self.repeatPasswordLabel = QLabel(Language.get("repeat_password"), parent)
        self.repeatPasswordLabel.setGeometry(15, 325, 340, 25)
        self.repeatPasswordLabel.hide()
        
        self.userQLineEdit = QLineEdit(parent)
        self.userQLineEdit.setGeometry(15, 150, 355, 50)
        self.userQLineEdit.setPlaceholderText(Language.get("enter_user_name"))

        self.passwordQLineEdit = QLineEdit(parent)
        self.passwordQLineEdit.setGeometry(15, 250, 355, 50)
        self.passwordQLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordQLineEdit.setPlaceholderText(Language.get("enter_password"))

        self.repeatPasswordQLineEdit = QLineEdit(parent)
        self.repeatPasswordQLineEdit.setGeometry(15, 355, 355, 50)
        self.repeatPasswordQLineEdit.setEchoMode(QLineEdit.Password)
        self.repeatPasswordQLineEdit.setPlaceholderText(Language.get("enter_password"))
        self.repeatPasswordQLineEdit.hide()

        self.logInButton = QPushButton(Language.get("log_in"), parent)
        self.logInButton.setGeometry(15, 490, 355, 50)

        self.registerButton = QPushButton(Language.get("register"), parent)
        self.registerButton.setGeometry(270, 555, 100, 30)

        self.accessOfflineButton = QPushButton(Language.get("access_offline"), parent)
        self.accessOfflineButton.setGeometry(15, 555, 150, 30)
        
        self.logInTitle.setFont(FONT_TITLE)
        self.logInTitle.setStyleSheet("font-weight: bold")
        self.logInTitle.setAlignment(Qt.AlignCenter)

        self.registerTitle.setFont(FONT_TITLE)
        self.registerTitle.setStyleSheet("font-weight: bold")
        self.registerTitle.setAlignment(Qt.AlignCenter)

        self.logInButton.setFont(FONT_BIG_TEXT)
        self.logInButton.setStyleSheet("background-color: #59CC4E; color: white; border: 0px")

        self.userLabel.setFont(FONT_TEXT)
        self.passwordLabel.setFont(FONT_TEXT)
        self.repeatPasswordLabel.setFont(FONT_TEXT)

        self.registerButton.setFont(FONT_SMALL_TEXT)
        self.registerButton.setStyleSheet("background-color: white; color: blue; border: 1px solid #AFAFAF")

        self.accessOfflineButton.setFont(FONT_SMALL_TEXT)
        self.accessOfflineButton.setStyleSheet("background-color: #DADADA; border: 1px solid #AFAFAF")

        self.userQLineEdit.setFont(FONT_SMALL_TEXT)
        self.userQLineEdit.setStyleSheet("border: 1px solid #CACACA; padding-left: 5px")

        self.passwordQLineEdit.setFont(FONT_SMALL_TEXT)
        self.passwordQLineEdit.setStyleSheet("border: 1px solid #CACACA; padding-left: 5px")

        self.repeatPasswordQLineEdit.setFont(FONT_SMALL_TEXT)
        self.repeatPasswordQLineEdit.setStyleSheet("border: 1px solid #CACACA; padding-left: 5px")

    def initEvents(self):
        self.logInButton.clicked.connect(self.checkLogging)
        self.registerButton.clicked.connect(self.changeToRegisterForm)
        self.accessOfflineButton.clicked.connect(self.openOfflineVersion)

    def checkLogging(self):
        authenticated = UserManager.authenticate(self.userQLineEdit.text(), self.passwordQLineEdit.text())

        if authenticated == 'NoInternet':
            self.accessOffline()
        elif authenticated != None:
            self.loggedSuccessful(self.userQLineEdit.text())
        else:
            self.loggedUnsuccessful()

    def changeToRegisterForm(self):
        self.logIn = not self.logIn

        self.logInButton.clicked.disconnect()

        if self.logIn:
            self.registerTitle.hide()
            self.repeatPasswordLabel.hide()
            self.repeatPasswordQLineEdit.hide()

            self.logInTitle.show()

            self.logInButton.clicked.connect(self.checkLogging)

            self.logInButton.setText(Language.get("log_in"))
            self.registerButton.setText(Language.get("register"))

            self.logInButton.setStyleSheet("background-color: #59CC4E; color: white; border: 0px")
            self.registerButton.setStyleSheet("background-color: white; color: blue; border: 1px solid #AFAFAF")
        else:
            self.logInTitle.hide()

            self.registerTitle.show()
            self.repeatPasswordLabel.show()
            self.repeatPasswordQLineEdit.show()

            self.logInButton.clicked.connect(self.register)

            self.logInButton.setText(Language.get("register"))
            self.registerButton.setText(Language.get("log_in"))

            self.registerButton.setStyleSheet("background-color: #59CC4E; color: white; border: 0px")
            self.logInButton.setStyleSheet("background-color: white; color: blue; border: 1px solid #AFAFAF")
        
    def register(self):
        if self.passwordQLineEdit.text().__len__() < 8 or self.repeatPasswordQLineEdit.text().strip().__len__() < 8:
            QMessageBox.warning(None, "Weak password", "The passwords must be 8 digits long")
        elif self.passwordQLineEdit.text() != self.repeatPasswordQLineEdit.text():
            QMessageBox.warning(None, "Diferent passwords", "The passwords must be the same")
        else:
            registred = UserManager.register(self.userQLineEdit.text(), self.passwordQLineEdit.text())

            if registred == 'NoInternet':
                self.accessOffline()
            elif registred == 'Duplicated':
                QMessageBox.warning(None, "Error: Duplicated", "The user already exists")
            elif registred != None:
                self.loggedSuccessful(self.userQLineEdit.text())
    
    def loggedUnsuccessful(self):
        QMessageBox.warning(None, "Login Failed", "Incorrect username or password.")

    def openOfflineVersion(self):
        UserManager.setUser('Guest', 'Offline')
        self.accessOffline()

    def accessOffline(self):
        if UserManager.username != 'Guest' and UserManager.role != 'Offline':
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.information(self, "You don't have internet connection", "There was an issue with the network")
        else:
            QMessageBox.information(self, "Offline version", "You opened the offline version")

        self.close()

        window.changeUserRole('Offline')

        Category.addCategory('Empty', 'white')
        Category.addCategory('Unreachable', 'red')
        Category.addCategory('Fill', 'green')

        createCategoryIn(window.categoryManager, 'Empty', window.widget, True)
        createCategoryIn(window.categoryManager, 'Unreachable', window.widget, True)
        createCategoryIn(window.categoryManager, 'Fill', window.widget, True)

        updateButtonsPosition(window.categoryManager, True)

        window.languageChanger.changeLang(self.languageChanger.language)
        window.languageChanger.setCurrentText(self.languageChanger.language)
        window.languageChanger.update()

        window.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))
        window.reOpenHome()
        window.show()
        
    def loggedSuccessful(self, username):
        [_, role] = UserManager.findUser(username)
        UserManager.setUser(username, role)

        window.changeUserRole(role)

        if UserManager.username == 'Guest' and UserManager.role == 'Offline':
            UserManager.setUser('Guest', 'Offline')
            QMessageBox.information(None, "You don't have internet connection", "There was an issue with the network")
        else:
            QMessageBox.information(None, "Login successful", "Login successful")

        self.close()

        getMongoInfo()

        window.languageChanger.update()
        window.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))
        window.reOpenHome()
        window.show()


def getMongoInfo():
    storeIndex = 0
    mongoCategories = 0

    try:
        for category in Mongo.CATEGORIES_COLLECTION.find({}):
            Category.addCategory(category['name'], category['color'])

            createCategoryIn(window.categoryManager, category['name'], window.widget, True)
            mongoCategories += 1
    except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
        UserManager.setUser('Guest', 'Offline')

        QMessageBox.warning(None, "Categories not found", "There was an issue with the network")

        mongoCategories = 0

    if mongoCategories <= 0:
        QMessageBox.warning(None, "You don't have any category in the database", "You'll use the default categories")

        Category.addCategory('Empty', 'white')
        Category.addCategory('Unreachable', 'red')
        Category.addCategory('Fill', 'green')

        createCategoryIn(window.categoryManager, 'Empty', window.widget, True)
        createCategoryIn(window.categoryManager, 'Unreachable', window.widget, True)
        createCategoryIn(window.categoryManager, 'Fill', window.widget, True)

        updateButtonsPosition(window.categoryManager, True)
        
    setEmptyCategory(window.categoryManager)

    try:
        for store in Mongo.STORES_COLLECTION.find({}):
            spacesInfo = []

            for index, shelf_id in enumerate(store['storeShelves']):
                shelf = Mongo.SHELVES_COLLECTION.find_one({ "_id": shelf_id })
                mongoSpaces = Mongo.SPACES_COLLECTION.find({"_id": {"$in": shelf['spaces']}})
                
                Shelf.createShelf(window.widget)

                SHELVES_FORMS[index].inputSpaces.setValue(shelf['spaces'].__len__() / store['storeFloors'])
                SHELVES_FORMS[index].shelfFloorsInput.setValue(shelf['floors'])
                SHELVES_FORMS[index].doubleShelfInput.setValue(shelf['double_shelf'])
                SHELVES_FORMS[index].hideForm()

                spacesInfo.append(mongoSpaces)
            
            saveShelfInfo()
            
            Store.createStore(store['name'], window.widget, store['image'])

            STORES[storeIndex].goBackStore.hide()

            for shelfIndex in range(store['storeShelves'].__len__()):
                for index, mongoSpace in enumerate(spacesInfo[shelfIndex]):
                    SHELVES[storeIndex][shelfIndex].spaces[index].mongo_id = mongoSpace['mongo_id']

                    if mongoCategories > 0:
                        category = Mongo.CATEGORIES_COLLECTION.find_one({ "_id": mongoSpace['category'] })
                        SHELVES[storeIndex][shelfIndex].spaces[index].categorySelector.setCurrentText(category['name'])
                        SHELVES[storeIndex][shelfIndex].spaces[index].category.name = category['name']
                        SHELVES[storeIndex][shelfIndex].spaces[index].category.color = category['color']
            
            storeIndex =+ 1
    except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout):
        UserManager.setUser('Guest', 'Offline')
        QMessageBox.warning(None, "Network error", "There was an issue with the network")

window = MainWindow()

class main():
    logInWindow = LogInWindow(window)
    logInWindow.show()
    
    sys.exit(app.exec_())

    Mongo.closeMongoConnection()

if __name__ == "__main__":
    main()
