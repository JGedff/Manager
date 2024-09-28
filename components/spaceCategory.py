from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QColorDialog

from utils.language import Language
from utils.category import Category
from utils.inputBool import InputBool
from utils.doubleButton import DoubleButton
from utils.functions.globalFunctions import updateNameCategory
from utils.functions.spaceCategoryFunctions import createCategoryIn, deleteCategoryFrom, updateButtonsPosition, setEmptyCategory

from constants import CATEGORY_NAMES, STORES

class SpaceCategory(QLabel):
    def __init__(self, space, parent):
        super().__init__(parent)

        self.initVariables(space, parent)
        self.initUI(parent)
        self.initEvents()

        setEmptyCategory(self)
        self.hideUI()

    def initVariables(self, space, parent):
        self.name = ''
        self.color = ''
        self.amount = 0
        self.newColor = ''
        self.SPACE = space
        self.doubleButtons = []
        self.mainParent = parent
        self.newCategoryName = ""
        self.newCategoryColor = ""
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

        self.saveCategory = QPushButton(Language.get("save"), parent)
        self.saveCategory.setGeometry(175, 125, 125, 25)
        self.saveCategory.hide()

        self.categoryColor = QPushButton(Language.get("select_color"), parent)
        self.categoryColor.setGeometry(175, 75, 125, 25)
        self.categoryColor.hide()

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

        self.newCategoryProductLabel = QLabel(Language.get("category_has_product"), parent)
        self.newCategoryProductLabel.setGeometry(posx + 225, posy - 100, 200, 25)
        self.newCategoryProductLabel.hide()

        self.newCategoryWithProduct = InputBool(Language.get("yes"), Language.get("no"), parent)
        self.newCategoryWithProduct.setGeometry(posx + 425, posy - 125, 100, 75)
        self.newCategoryWithProduct.hide()

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
        self.SPACE.updateSpaceColor()
        self.SPACE.updateScroll()

        self.showUI()
        self.SPACE.openSpaceConfig.show()
        self.showSpace.hide()
        self.categoryNameLabel.hide()
        self.categoryColorLabel.hide()
        self.saveCategory.hide()
        self.categoryColor.hide()
        self.categoryName.hide()

    def showUI(self):
        for button in self.doubleButtons:
            button.show()

        self.addCategory.show()

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
        self.SPACE.openSpaceConfig.hide()
        self.SPACE.updateScrollToDefault()
            
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
        self.SPACE.STORE.WINDOW.goHome.hide()

    def hideUI(self):
        for button in self.doubleButtons:
            button.hide()
        
        self.addCategory.hide()

    
    def saveInfo(self):
        newName = self.categoryName.text()

        if newName != "":
            self.reloadNameCategories(newName)

        if self.newColor != "" and newName != "":
            self.reloadColorCategories(newName)
        elif self.newColor != "":
            self.reloadColorCategories(self.nameModifiedCategory)

    def reloadNameCategories(self, newName):
        index = Category.getIndexByName(self.nameModifiedCategory)
        Category.changeCategoryName(index, newName)

        updateNameCategory(STORES[0].WINDOW.configCategory, self.colorModifiedCategory, self.nameModifiedCategory, newName, index)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    updateNameCategory(space, self.colorModifiedCategory, self.nameModifiedCategory, newName, index)

    def reloadColorCategories(self, newName):
        index = Category.getIndexByName(newName)
        Category.changeCategoryColor(index, self.newColor)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.name == newName:
                        space.category.color = self.newColor

    def showAddCategory(self):
        self.creatingCategory = True

        self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 100)
        self.addCategoryName.move(self.addCategory.pos().x(), self.addCategory.pos().y() - 100)
        self.createCategoryButton.move(self.addCategory.pos().x() + 400, self.addCategory.pos().y() - 50)
        self.newCategoryColorButton.move(self.addCategory.pos().x() + 225, self.addCategory.pos().y() - 50)
        self.newCategoryWithProduct.move(self.addCategory.pos().x() + 400, self.addCategory.pos().y() - 125)
        self.cancelButtonAddCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() - 50)
        self.newCategoryProductLabel.move(self.addCategory.pos().x() + 225, self.addCategory.pos().y() - 100)

        self.addCategory.setDisabled(True)

        self.addCategoryName.show()
        self.createCategoryButton.show()
        self.newCategoryColorButton.show()
        self.newCategoryWithProduct.show()
        self.newCategoryProductLabel.show()
        self.cancelButtonAddCategory.show()

        for button in self.doubleButtons:
            button.setDisabledButton2(True)

    def cancelAddCategory(self):
        self.addCategoryName.hide()
        self.createCategoryButton.hide()
        self.newCategoryColorButton.hide()
        self.newCategoryWithProduct.hide()
        self.newCategoryProductLabel.hide()
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
            self.newCategoryWithProduct.move(self.newCategoryWithProduct.pos().x(), self.newCategoryWithProduct.pos().y() - 100)
            self.cancelButtonAddCategory.move(self.cancelButtonAddCategory.pos().x(), self.cancelButtonAddCategory.pos().y() - 100)
            self.newCategoryProductLabel.move(self.newCategoryProductLabel.pos().x(), self.newCategoryProductLabel.pos().y() - 100)

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
        Category.addCategory(self.newCategoryName.capitalize(), self.newCategoryColor, self.newCategoryWithProduct.getValue())

        createCategoryIn(STORES[0].WINDOW.configCategory, self.newCategoryName.capitalize(), self.mainParent)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    createCategoryIn(space, self.newCategoryName.capitalize(), self.mainParent)
        
        self.showUI()
        self.cancelAddCategory()

        self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 100)
        self.addCategoryName.move(self.addCategoryName.pos().x(), self.addCategoryName.pos().y() + 50)
        self.createCategoryButton.move(self.createCategoryButton.pos().x(), self.createCategoryButton.pos().y() + 50)
        self.newCategoryColorButton.move(self.newCategoryColorButton.pos().x(), self.newCategoryColorButton.pos().y() + 50)
        self.newCategoryWithProduct.move(self.newCategoryWithProduct.pos().x(), self.newCategoryWithProduct.pos().y() + 50)
        self.cancelButtonAddCategory.move(self.cancelButtonAddCategory.pos().x(), self.cancelButtonAddCategory.pos().y() + 50)
        self.newCategoryProductLabel.move(self.newCategoryProductLabel.pos().x(), self.newCategoryProductLabel.pos().y() + 50)

        self.SPACE.updateScroll()
    
    def deleteCategory(self):
        indexButtonPressed = 0
        
        for index, send in enumerate(self.doubleButtons):
            if send.button2 == self.sender():
                indexButtonPressed = index

        categoryName = Category.getNameByIndex(indexButtonPressed)
        Category.delCategory(indexButtonPressed)

        deleteCategoryFrom(STORES[0].WINDOW.configCategory, indexButtonPressed, categoryName.capitalize())
        updateButtonsPosition(STORES[0].WINDOW.configCategory)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.doubleButtons.__len__() > CATEGORY_NAMES.__len__():
                        deleteCategoryFrom(space, indexButtonPressed, categoryName)
                        updateButtonsPosition(space)

        self.SPACE.updateScroll()
