from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox

from constants import CATEGORY_NAMES, SHELVES, STORES

from utils.categorySpaces import SpaceCategory

class Space(QLabel):
    def __init__(self, posx, posy, actualFloor, shelf, store, window, parent, long = False, buttonFromMain = False):
        super().__init__(parent)

        self.WINDOW = window
        self.STORE = store
        self.SHELF = shelf
        self.actualFloor = actualFloor
        self.category = SpaceCategory(self, parent)
        self.long = long
        self.buttonFromMain = buttonFromMain

        if actualFloor > self.SHELF.floors:
            self.category.setUnreachableCategory()

        self.setGeometry(posx, posy, 75, 75)
        self.initUI(parent)
        self.initEvents()
        
    def initUI(self, parent):
        self.box = QPushButton(parent)

        if self.long:
            self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 151)
        else:
            self.box.setGeometry(self.pos().x() + 1, self.pos().y() + 1, 76, 76)
    
        self.box.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")

        self.openSpaceConfig = QPushButton("← Go back", parent)
        self.openSpaceConfig.setGeometry(1300, 15, 100, 50)
        
        self.configBox = QPushButton(parent)
        self.configBox.setGeometry(26, 26, 76, 76)
        self.configBox.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")

        self.labelCategory = QLabel("Category:", parent)
        self.labelCategory.setGeometry(150, 26, 50, 25)

        self.configCategory = QComboBox(parent)
        self.configCategory.setGeometry(200, 26, 100, 25)
        self.configCategory.addItem(self.category.name)

        for category in CATEGORY_NAMES:
            if category != self.category.name:
                self.configCategory.addItem(category.capitalize())


        if self.buttonFromMain:
            self.editCategories = QPushButton("Edit categories ⚙️", parent)
            self.editCategories.setGeometry(1316, 610, 100, 30)
        else:
            self.editCategories = QPushButton("⚙️", parent)
            self.editCategories.setGeometry(300, 26, 26, 26)

    def changeCategory(self):
        self.category.setCategoryByName(self.configCategory.currentText())
        self.configBox.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")

    def initEvents(self):
        self.box.clicked.connect(self.configSpace)
        self.openSpaceConfig.clicked.connect(self.configSpace)
        self.editCategories.clicked.connect(self.openConfigCategories)
        self.configCategory.currentTextChanged.connect(self.changeCategory)

    def configSpace(self):
        if self.buttonFromMain:
            self.home()
            self.openSpaceConfig.hide()

            self.WINDOW.addStoreButton.show()

            for i in STORES:
                i.showIcon()
        else:
            self.STORE.configSpace()
            self.configBox.show()
            self.configCategory.show()
            self.labelCategory.show()
            self.editCategories.show()
            self.openSpaceConfig.hide()

        self.category.hideUI()

    def hideSpace(self):
        self.box.hide()
        self.configBox.hide()
        self.configCategory.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category.hideUI()

    def showFloor(self, number):
        if number != self.actualFloor:
            self.hideSpace()
        else:
            self.showSpace()

    def showSpace(self):
        self.box.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")
        self.configBox.setStyleSheet("background-color: " + self.category.color + "; border: 1px solid black")
        self.box.show()
        self.configBox.hide()

        self.configCategory.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category.hideUI()

    def openConfigCategories(self):
        self.box.hide()
        self.configBox.hide()
        self.labelCategory.hide()
        self.configCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.show()
        self.category.showUI()

        self.STORE.configCategories()

        if self.buttonFromMain:
            self.WINDOW.addStoreButton.hide()

            for i in SHELVES:
                i.hideForm()

            for i in STORES:
                i.hideIcon()

    def home(self):
        self.editCategories.show()

    def hideHome(self):
        self.editCategories.hide()