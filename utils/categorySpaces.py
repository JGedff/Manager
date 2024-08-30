from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QColorDialog

from constants import CATEGORY_NAMES, CATEGORY_COLORS, STORES

class Category():
    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategory(index, name, color):
        CATEGORY_NAMES[index] = name
        CATEGORY_COLORS[index] = color

    def addCategory(name, color):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)

    def delCategory(index):
        CATEGORY_NAMES.pop(index)
        CATEGORY_COLORS.pop(index)

    def getCategoryByIndex(index):
        return CATEGORY_NAMES[index], CATEGORY_COLORS[index]
    
    def getCategoryByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return cat, CATEGORY_COLORS[index]

    def getIndexByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index

    def getCategoryByColor(color):
        for index, cat in enumerate(CATEGORY_COLORS):
            if cat.lower() == color.lower():
                return CATEGORY_NAMES[index], cat
        
    def getNameByColor(color):
        for index, cat in enumerate(CATEGORY_COLORS):
            if cat.lower() == color.lower():
                return CATEGORY_NAMES[index]
            
    def getColorByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]

class SpaceCategory():
    def __init__(self, space, parent):
        self.SPACE = space
        self.nameCategory = ''
        self.name = ''
        self.color = ''
        self.product = None
        self.amount = 0
        self.buttons = []
        
        self.initUI(parent)
        self.initEvents()
        self.hideUI()

        self.setEmptyCategory()

    def initUI(self, parent):
        posx = 25
        posy = 25

        self.showSpace = QPushButton("← Go back", parent)
        self.showSpace.setGeometry(1300, 15, 100, 50)
        self.showSpace.hide()

        self.categoryNameLabel = QLabel("Category name:", parent)
        self.categoryNameLabel.setGeometry(25, 25, 125, 25)
        self.categoryNameLabel.hide()

        self.categoryName = QLineEdit(parent)
        self.categoryName.setGeometry(175, 25, 125, 25)
        self.categoryName.hide()
        
        self.categoryColorLabel = QLabel("Category color:", parent)
        self.categoryColorLabel.setGeometry(25, 75, 125, 25)
        self.categoryColorLabel.hide()

        self.categoryColor = QPushButton("Select color", parent)
        self.categoryColor.setGeometry(175, 75, 125, 25)
        self.categoryColor.hide()

        for category in CATEGORY_NAMES:
            newButton = QPushButton(category.capitalize(), parent)
            newButton.setGeometry(posx, posy, 200, 25)
            newButton.clicked.connect(self.editCategory)

            posy += 50

            self.buttons.append(newButton)

    def initEvents(self):
        self.showSpace.clicked.connect(self.stopEditCategory)
        self.categoryColor.clicked.connect(self.selectColor)

    def selectColor(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.categoryColor.setStyleSheet("background-color: " + color.name())
            index = Category.getIndexByName(self.nameCategory)
            Category.changeCategoryColor(index, color.name())
    
    def reloadColorCategories(self):
        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.name == self.nameCategory:
                        space.category.color = CATEGORY_COLORS[Category.getIndexByName(self.nameCategory)]
                        space.category.name = CATEGORY_COLORS[Category.getIndexByName(self.name)]

    def stopEditCategory(self):
        self.reloadColorCategories()

        self.showUI()
        self.SPACE.openSpaceConfig.show()
        self.showSpace.hide()
        self.categoryNameLabel.hide()
        self.categoryColorLabel.hide()
        self.categoryColor.hide()
        self.categoryName.hide()

    def editCategory(self):
        self.hideUI()
        self.SPACE.openSpaceConfig.hide()
        self.showSpace.show()

        color = Category.getColorByName(self.buttons[0].sender().text())
        self.nameCategory = self.buttons[0].sender().text()

        self.categoryColor.setStyleSheet("background-color: " + color)

        self.categoryNameLabel.show()
        self.categoryColorLabel.show()
        self.categoryColor.show()
        self.categoryName.show()
    
    def setEmptyCategory(self):
        self.name = CATEGORY_NAMES[0]
        self.color = CATEGORY_COLORS[0]
        self.nameCategory = CATEGORY_NAMES[0]

    def setUnreachableCategory(self):
        self.name = CATEGORY_NAMES[1]
        self.color = CATEGORY_COLORS[1]
        self.nameCategory = CATEGORY_NAMES[1]
    
    def setCategoryByName(self, name):
        self.name = name
        self.color = Category.getColorByName(name)
        self.nameCategory = name

    def setCategoryByColor(self, color):
        self.color = color
        self.name = Category.getNameByColor(color)
        self.nameCategory = self.name

    def hideUI(self):
        for button in self.buttons:
            button.hide()

    def showUI(self):
        for button in self.buttons:
            button.show()