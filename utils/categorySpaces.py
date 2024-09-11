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

    def getNameByIndex(index):
        return CATEGORY_NAMES[index]

class SpaceCategory():
    def __init__(self, space, parent):
        self.initVariables(space, parent)
        self.initUI(parent)
        self.initEvents()

        self.setEmptyCategory()
        self.hideUI()

    def initVariables(self, space, parent):
        self.name = ''
        self.color = ''
        self.amount = 0
        self.buttons = []
        self.newColor = ''
        self.SPACE = space
        self.product = None
        self.deleteButtons = []
        self.mainParent = parent
        self.newCategoryName = ""
        self.newCategoryColor = ""
        self.creatingCategory = False
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

            deleteButton = QPushButton("🗑️", parent)
            deleteButton.setGeometry(posx + 225, posy, 200, 25)

            posy += 50

            self.buttons.append(newButton)
            self.deleteButtons.append(deleteButton)

        self.addCategory = QPushButton("+ Add category", parent)
        self.addCategory.setGeometry(posx, posy, 200, 50)
        self.addCategory.hide()

        self.addCategoryName = QLineEdit(parent)
        self.addCategoryName.setGeometry(posx, posy, 200, 25)
        self.addCategoryName.hide()

        self.newCategoryColorButton = QPushButton("Select color", parent)
        self.newCategoryColorButton.setGeometry(posx + 225, posy, 125, 25)
        self.newCategoryColorButton.hide()

        self.cancelButtonAddCategory = QPushButton("Cancel", parent)
        self.cancelButtonAddCategory.setGeometry(posx, posy + 50, 100, 25)
        self.cancelButtonAddCategory.hide()

        self.createCategoryButton = QPushButton("Create", parent)
        self.createCategoryButton.setGeometry(posx + 125, posy + 50, 100, 25)
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

        for button in self.buttons:
            button.clicked.connect(self.editCategory)

        for button in self.deleteButtons:
            button.clicked.connect(self.deleteCategory)

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

        for button in self.deleteButtons:
            button.show()
        
        self.addCategory.show()

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

        for button in self.deleteButtons:
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

    def showAddCategory(self):
        self.creatingCategory = True

        self.addCategoryName.move(self.addCategory.pos().x(), self.addCategory.pos().y())
        self.newCategoryColorButton.move(self.addCategory.pos().x() + 225, self.addCategory.pos().y())
        self.cancelButtonAddCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 50)
        self.createCategoryButton.move(self.addCategory.pos().x() + 225, self.addCategory.pos().y() + 50)

        self.addCategory.move(self.addCategory.pos().x(), self.addCategory.pos().y() + 100)
        self.addCategory.setDisabled(True)

        self.addCategoryName.show()
        self.newCategoryColorButton.show()
        self.createCategoryButton.show()
        self.cancelButtonAddCategory.show()

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

        self.createCategoryIn(STORES[0].WINDOW.categorySpace)

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    self.createCategoryIn(space)
        
        self.showUI()
        self.creatingCategory = False
        self.cancelAddCategory()
    
    def createCategoryIn(self,space):
        newButton = QPushButton(self.newCategoryName.capitalize(), self.mainParent)
        newButton.setGeometry(25, 50 * CATEGORY_NAMES.__len__() - 25, 200, 25)
        newButton.clicked.connect(space.category.editCategory)

        newDeleteButton = QPushButton("🗑️", self.mainParent)
        newDeleteButton.setGeometry(250, 50 * CATEGORY_NAMES.__len__() - 25, 200, 25)
        newDeleteButton.clicked.connect(space.category.deleteCategory)

        space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)
        space.category.buttons.append(newButton)
        space.category.deleteButtons.append(newDeleteButton)
        space.configCategory.addItem(self.newCategoryName.capitalize())

    def deleteCategory(self):
        indexButtonPressed = int((self.buttons[0].sender().pos().y() - 25) / 50)
        categoryName = Category.getNameByIndex(indexButtonPressed)
        Category.delCategory(indexButtonPressed)

        self.deleteCategoryFrom(STORES[0].WINDOW.categorySpace, indexButtonPressed, categoryName.capitalize())

        for store in STORES:
            for shelf in store.shelves:
                for space in shelf.spaces:
                    if space.category.buttons.__len__() > CATEGORY_NAMES.__len__():
                        self.deleteCategoryFrom(space, indexButtonPressed, categoryName)

    def deleteCategoryFrom(self, space, indexButtonPressed, categoryName):
        items = []

        for index in range(space.configCategory.count()):
            items.append(space.configCategory.itemText(index))

        for index, item in enumerate(items):
            if item == categoryName:
                space.configCategory.removeItem(index)


        space.category.buttons[indexButtonPressed].hide()
        space.category.deleteButtons[indexButtonPressed].hide()
        
        space.category.buttons.pop(indexButtonPressed)
        space.category.deleteButtons.pop(indexButtonPressed)
        space.category.addCategory.move(25, 50 * CATEGORY_NAMES.__len__() + 25)

    def setEmptyCategory(self):
        self.name = CATEGORY_NAMES[0]
        self.color = CATEGORY_COLORS[0]

    def setUnreachableCategory(self):
        self.name = CATEGORY_NAMES[1]
        self.color = CATEGORY_COLORS[1]
    
    def setCategoryByName(self, name):
        self.name = name
        self.color = Category.getColorByName(name)