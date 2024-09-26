from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox

from constants import CATEGORY_NAMES, WINDOW_WIDTH, WINDOW_HEIGHT

from components.spaceProduct import SpaceProduct
from components.spaceCategory import SpaceCategory

from utils.language import Language
from utils.functions.spaceCategoryFunctions import setUnreachableCategory, setCategoryByName

class Space(QLabel):
    def __init__(self, posx, posy, actualFloor, floors, store, parent, long = False, buttonFromMain = False, times5Space = 0):
        super().__init__(parent)

        self.setGeometry(posx, posy, 75, 75)

        self.initVariables(actualFloor, floors, store, parent, long, buttonFromMain)
        self.initUI(parent, times5Space)
        self.initEvents()
        
    def initVariables(self, actualFloor, floors, store, parent, long, buttonFromMain):
        self.long = long
        self.STORE = store
        self.widget = parent
        self.actualFloor = actualFloor
        self.buttonFromMain = buttonFromMain
        self.category = SpaceCategory(self, parent)
        self.product = SpaceProduct(self.category, parent)

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

        self.configCategory = QComboBox(parent)
        self.configCategory.setGeometry(210, 26, 100, 25)
        self.configCategory.addItem(self.category.name)

        for category in CATEGORY_NAMES:
            if category != self.category.name:
                self.configCategory.addItem(category.capitalize())

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
        self.configCategory.currentTextChanged.connect(self.changeCategory)

    def configSpace(self):
        if self.buttonFromMain:
            self.openConfigCategories()
        else:
            self.STORE.configSpace()
            self.configBox.show()
            self.labelCategory.show()
            self.configCategory.show()
            self.editCategories.show()
            self.product.show()
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
            
    def openConfigCategories(self):
        if self.buttonFromMain:
            self.openSpaceConfig.show()
            self.category.showUI()
        else:
            self.product.hide()
            self.configBox.hide()
            self.labelCategory.hide()
            self.configCategory.hide()
            self.editCategories.hide()
            self.openSpaceConfig.show()
            self.category.showUI()
            self.STORE.configCategories()
    
    def stopConfigSpace(self):
        if self.buttonFromMain:
            self.category.hideUI()
            self.openSpaceConfig.hide()
            self.STORE.WINDOW.reOpenHome()
        else:
            self.category.cancelAddCategory()
            self.STORE.configSpace()
            self.configBox.show()
            self.product.show()
            self.labelCategory.show()
            self.editCategories.show()
            self.configCategory.show()
    
    def changeCategory(self, category):
        setCategoryByName(self.category, category)
        self.product.categoryChanged()
        self.updateSpaceColor()

    def showFloor(self, number):
        if number != self.actualFloor:
            self.hideSpace()
        else:
            self.showSpace()

    def hideSpace(self):
        self.box.hide()
        self.product.hide()
        self.configBox.hide()
        self.configCategory.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()
        self.category.hideUI()

    def showSpace(self):
        self.updateSpaceColor()
        self.box.show()
        self.product.hide()
        self.configBox.hide()

        self.configCategory.hide()
        self.labelCategory.hide()
        self.editCategories.hide()
        self.openSpaceConfig.hide()

    def home(self):
        self.editCategories.show()

    def hideHome(self):
        self.editCategories.hide()