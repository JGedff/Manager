from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QColorDialog

from constants import CATEGORY_NAMES, CATEGORY_COLORS, STORES

class Category():
    def changeCategoryColor(index, color):
        CATEGORY_COLORS[index] = color

    def changeCategoryName(index, name):
        CATEGORY_NAMES[index] = name

    def addCategory(name, color):
        CATEGORY_NAMES.append(name)
        CATEGORY_COLORS.append(color)

    def delCategory(index):
        CATEGORY_NAMES.pop(index)
        CATEGORY_COLORS.pop(index)

    def getIndexByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return index

    def getColorByName(name):
        for index, cat in enumerate(CATEGORY_NAMES):
            if cat.lower() == name.lower():
                return CATEGORY_COLORS[index]

    def getIndexByColor(color):
        for index, cat in enumerate(CATEGORY_COLORS):
            if cat.lower() == color.lower():
                return index

class SpaceCategory():
    def __init__(self, space, parent):
        self.initVariables(space)
        self.initUI(parent)
        self.initEvents()

        self.setEmptyCategory()
        self.hideUI()

    def initVariables(self, space):
        self.name = ''
        self.color = ''
        self.amount = 0
        self.buttons = []
        self.newColor = ''
        self.SPACE = space
        self.product = None
        self.nameModifiedCategory = ''
        self.colorModifiedCategory = ""

    def initUI(self, parent):
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

        self.saveCategory = QPushButton("Save", parent)
        self.saveCategory.setGeometry(175, 125, 125, 25)
        self.saveCategory.hide()

        self.categoryColor = QPushButton("Select color", parent)
        self.categoryColor.setGeometry(175, 75, 125, 25)
        self.categoryColor.hide()

        posx = 25
        posy = 25

        for category in CATEGORY_NAMES:
            newButton = QPushButton(category.capitalize(), parent)
            newButton.setGeometry(posx, posy, 200, 25)

            posy += 50

            self.buttons.append(newButton)

    def initEvents(self):
        self.showSpace.clicked.connect(self.stopEditCategory)
        self.categoryColor.clicked.connect(self.selectColor)
        self.saveCategory.clicked.connect(self.saveInfo)

        for button in self.buttons:
            button.clicked.connect(self.editCategory)

    def stopEditCategory(self):
        self.SPACE.updateSpaceColor()

        self.showUI()
        self.SPACE.openSpaceConfig.show()
        self.showSpace.hide()
        self.categoryNameLabel.hide()
        self.categoryColorLabel.hide()
        self.saveCategory.hide()
        self.categoryColor.hide()
        self.categoryName.hide()

    def showUI(self):
        for button in self.buttons:
            button.show()

    def selectColor(self):
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.categoryColor.setStyleSheet("background-color: " + color.name())
            self.newColor = color.name()
    
    def editCategory(self):
        self.hideUI()
        self.SPACE.openSpaceConfig.hide()
        self.showSpace.show()
        self.newColor = ''
            
        # self.buttons[0].sender() will be used as a receptor of events
        self.nameModifiedCategory = self.buttons[0].sender().text()
        color = Category.getColorByName(self.nameModifiedCategory)
        self.colorModifiedCategory = color

        self.categoryColor.setStyleSheet("background-color: " + color)

        self.categoryNameLabel.show()
        self.categoryColorLabel.show()
        self.saveCategory.show()
        self.categoryColor.show()
        self.categoryName.show()
        self.SPACE.STORE.WINDOW.goBackHomeButton.hide()

    def hideUI(self):
        for button in self.buttons:
            button.hide()
    
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

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.color == self.colorModifiedCategory:
                        for button in space.category.buttons:
                            if button.text() == self.nameModifiedCategory:
                                button.setText(newName)

                        space.configCategory.setItemText(0, newName)
                        space.category.name = newName
                    else:
                        for button in space.category.buttons:
                            if button.text() == self.nameModifiedCategory:
                                button.setText(newName)

                        space.configCategory.setItemText(index, newName)

    def reloadColorCategories(self, newName):
        index = Category.getIndexByName(newName)
        Category.changeCategoryColor(index, self.newColor)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.name == newName:
                        space.category.color = self.newColor

    def setEmptyCategory(self):
        self.name = CATEGORY_NAMES[0]
        self.color = CATEGORY_COLORS[0]

    def setUnreachableCategory(self):
        self.name = CATEGORY_NAMES[1]
        self.color = CATEGORY_COLORS[1]
    
    def setCategoryByName(self, name):
        self.name = name
        self.color = Category.getColorByName(name)