import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QColorDialog

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS, STORES, DEFAULT_IMAGE, SHELVES, DEFAULT_SPACE_MARGIN, CATEGORY_NAMES

from utils.functions.globalFunctions import getMaxFloor
from utils.functions.shelfFunctions import saveShelfInfo, updateShelfPosition
from utils.functions.spaceCategoryFunctions import setUnreachableCategory, setCategoryByName, createCategoryIn, updateNameCategory, deleteCategoryFrom, updateButtonsPosition, setEmptyCategory

from utils.language import Language
from utils.category import Category
from utils.imageButton import ImageButton
from utils.doubleButton import DoubleButton

from components.shelf import Shelf
from components.languageChanger import LanguageChanger

app = QApplication(sys.argv)

class SpaceCategory(QLabel):
    def __init__(self, storeIndex = 0, shelfIndex = 0, spaceIndex = 0, parent = None, shortcut = False):
        super().__init__(parent)

        self.initVariables(storeIndex, shelfIndex, spaceIndex, parent, shortcut)
        self.initUI(parent)
        self.initEvents()

        setEmptyCategory(self)

    def initVariables(self, storeIndex, shelfIndex, spaceIndex, parent, shortcut):
        self.name = ''
        self.color = ''
        self.newColor = ''
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

        for index, category in enumerate(CATEGORY_NAMES):
            if index > 2:
                newDoubleButton = DoubleButton(posx, posy, category.capitalize(), "🗑️", self.editCategory, self.deleteCategory, parent)
                posy += 50

                self.doubleButtons.append(newDoubleButton)
            else:
                newDoubleButton = DoubleButton(posx, posy, category.capitalize(), "", self.editCategory, self.deleteCategory, parent)

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
            SHELVES[self.storeIndex][self.shelfIndex].spaces[self.spaceIndex + 1].openSpaceConfig.show()

    def showUI(self):
        for button in self.doubleButtons:
            button.show()

        self.addCategory.show()

        if self.shortcut:
            window.goHome.hide()

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

        if self.newColor != "" and newName != "":
            self.reloadColorCategories(newName)
        elif self.newColor != "":
            self.reloadColorCategories(self.nameModifiedCategory)

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

        deleteCategoryFrom(window.categoryManager, indexButtonPressed, categoryName, True)
        updateButtonsPosition(window.categoryManager, True)

        for store in SHELVES:
            for shelf in store:
                for space in shelf.spaces:
                    if space.category.doubleButtons.__len__() > CATEGORY_NAMES.__len__():
                        deleteCategoryFrom(space, indexButtonPressed, categoryName)
                        updateButtonsPosition(space)

class Space(QLabel):
    def __init__(self, posx, posy, actualFloor, floors, storeIndex, shelfIndex, spaceIndex, parent = None, long = False, times5Space = 0):
        super().__init__(parent)

        self.setGeometry(posx, posy, 75, 75)

        self.initVariables(actualFloor, floors, storeIndex, shelfIndex, spaceIndex, parent, long)
        self.initUI(parent, times5Space)
        self.initEvents()
        
    def initVariables(self, actualFloor, floors, storeIndex, shelfIndex, spaceIndex, parent, long):
        self.long = long
        self.storeIndex = storeIndex
        self.actualFloor = actualFloor
        self.category = SpaceCategory(storeIndex, shelfIndex, spaceIndex, parent)

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
        self.editCategories.setGeometry(320, 26, 26, 26)

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
        setCategoryByName(self.category, category)
        self.updateSpaceColor()

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
                mod = self.spacesLength % 2
                sideSpaces = (self.spacesLength / 2).__trunc__()

                for index in range(sideSpaces):
                    if (index + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent, False, times5))

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy + DEFAULT_SPACE_MARGIN, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent))
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent, True, times5))
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.storeIndex, self.actualNumber - 1, index, parent, False, False, times5))

    def initEvents(self):
        updateShelfPosition()
        window.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalInfoPosition)

    def updateHorizontalInfoPosition(self, value):
        self.shelfNumber.move(value + int(WINDOW_WIDTH / 2 - self.shelfNumber.width() / 2), self.shelfNumber.pos().y())

class Store():
    @staticmethod
    def createStore(storeName, parent):
        saveShelfInfo()

        posx = 25
        posy = 25
            
        for _ in STORES:
            posx += 170

            if posx + 170 >= WINDOW_WIDTH:
                posx = 25
                posy += 170

        STORES.append(Store(storeName, DEFAULT_IMAGE, posx, posy, parent))

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initVariables()
        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeHeightScroll()

    def initVariables(self):
        # Window config
        self.setWindowTitle(Language.get("window_title"))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add scroll to window
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

        self.categoryManager = SpaceCategory(0, 0, 0, self.widget, True)

    def initUI(self, parent):
        # Main buttons
        self.languageChanger = LanguageChanger(self, parent)

        self.goHome = QPushButton(Language.get("go_back"), parent)
        self.goHome.setGeometry(1300, 10, 100, 50)
        self.goHome.hide()

        self.addStoreButton = QPushButton(Language.get("add_store"), parent)
        self.addStoreButton.setGeometry(WINDOW_WIDTH - 135, WINDOW_HEIGHT - 75, 110, 50)

        self.editCategories = QPushButton(Language.get("edit_categories"), parent)
        self.editCategories.setGeometry(WINDOW_WIDTH - 135, 610, 110, 30)

        # Header Form
        self.headerFormBackground = QLabel("", parent)
        self.headerFormBackground.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.headerFormBackground.setStyleSheet("background-color: #dddddd;")
        self.headerFormBackground.hide()

        self.storeNameLabel = QLabel(Language.get("name_store"), parent)
        self.storeNameLabel.setGeometry(400, 20, 100, 35)
        self.storeNameLabel.hide()
        
        self.storeNameInput = QLineEdit(parent)
        self.storeNameInput.setGeometry(800, 20, 300, 35)
        self.storeNameInput.setPlaceholderText(Language.get("store") + str(1))
        self.storeNameInput.hide()

        # Footer form
        self.footerFormBackground = QLabel("", parent)
        self.footerFormBackground.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.footerFormBackground.setStyleSheet("background-color: #dddddd;")
        self.footerFormBackground.hide()

        self.addShelfButton = QPushButton(Language.get("add_shelf"), parent)
        self.addShelfButton.setGeometry(830, WINDOW_HEIGHT - 62, 100, 50)
        self.addShelfButton.hide()

        self.createStoreButton = QPushButton(Language.get("create_store"), parent)
        self.createStoreButton.setGeometry(1000, WINDOW_HEIGHT - 62, 100, 50)
        self.createStoreButton.hide()

        Store.showAllStoreIcons()

    def initEvents(self):
        # Click buttons
        self.goHome.clicked.connect(self.reOpenHome)
        self.addStoreButton.clicked.connect(self.addStore)
        self.addShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.saveStoreInfo)
        self.editCategories.clicked.connect(self.configCategories)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)
    
    # Scroll functions
    def updateVerticalHeaderPosition(self, value):
        self.goHome.move(self.goHome.pos().x(), value + 10)
        self.editCategories.move(self.editCategories.pos().x(), value + 610)
        self.storeNameInput.move(self.storeNameInput.pos().x(), value + 20)
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
            if SHELVES_FORMS.__len__() > 0 and SHELVES_FORMS[SHELVES_FORMS.__len__() - 1].pos().y() + 250 > WINDOW_HEIGHT:
                self.widget.resize(WINDOW_WIDTH - 20, SHELVES_FORMS[SHELVES_FORMS.__len__() - 1].pos().y() + 250)
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
        if STORES.__len__() < 26:
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
        storeName = self.storeNameInput.text().strip()

        if storeName == "":
            storeName = Language.get("store") + str(STORES.__len__() + 1)

        Shelf.hideAllForms()
        Store.createStore(storeName, self.widget)

        self.storeNameInput.setText("")
        self.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))

        self.reOpenHome()
        self.goHome.raise_()
    
    def configCategories(self):
        Store.hideAllStoreIcons()

        self.categoryManager.showUI()

        self.hideMainButtons()

    # Show objects
    def showAddStoreForm(self):
        self.headerFormBackground.show()
        self.footerFormBackground.show()
        self.createStoreButton.show()
        self.storeNameInput.show()
        self.storeNameLabel.show()
        self.addShelfButton.show()

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

window = MainWindow()

class main():
    window.categoryManager.hideUI()
    window.goHome.hide()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
