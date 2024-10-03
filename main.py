import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QComboBox, QPushButton

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS, STORES, DEFAULT_IMAGE, SHELVES, DEFAULT_SPACE_MARGIN

from utils.functions.globalFunctions import getMaxFloor
from utils.functions.shelfFunctions import saveShelfInfo, updateShelfPosition

from utils.language import Language
from utils.imageButton import ImageButton

from components.space import Space
from components.shelf import Shelf
from components.languageChanger import LanguageChanger

app = QApplication(sys.argv)

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

    def __init__(self, posx, posy, floors, spaces, double_shelf, storeFloors, shelfNumber = 1, parent = None):
        self.initVariables(posx, floors, spaces, double_shelf, storeFloors, shelfNumber)
        self.initUI(posx, posy, parent)
        self.initEvents()
    
    def initVariables(self, posx, floors, spaces, double_shelf, storeFloors, shelfNumber):
        self.spaces = []
        self.posx = posx
        self.storeFloors = storeFloors
        self.floors = floors
        self.actualNumber = shelfNumber
        self.spacesLength = spaces
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
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, parent, False, False, times5))

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy + DEFAULT_SPACE_MARGIN, actualFloor + 1, self.floors, parent))
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, parent, True, False, times5))
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, parent, False, False, times5))

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

    def __init__(self, name, image, posx, posy, parent):
        self.setupStore(parent)
        self.initUI(name, image, posx, posy, parent)
        self.initEvents()
    
    def setupStore(self, parent):
        self.indexShelves = SHELVES.__len__()
        self.floor = getMaxFloor()
        storeShelves = []

        for index, i in enumerate(SHELVES_FORMS):
            storeShelves.append(ShelfInfo(25, 50 + (185 * index), i.floors, i.spaces, i.double_shelf, self.floor, (index + 1), parent))
        
        SHELVES.append(storeShelves)
        SHELVES_FORMS.clear()
        
        Shelf.createShelf(parent)
        Shelf.hideAllForms()

    def initUI(self, name, image, posx, posy, parent):
        self.goBackStore = QPushButton(Language.get("go_back"), parent)
        self.goBackStore.setGeometry(1300, 15, 100, 50)
        self.goBackStore.hide()

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
        ShelfInfo.changeFloor(self.indexShelves, int(floor.split(' ')[1]))

    def updateVerticalHeaderPosition(self, value):
        self.changeFloorButton.move(self.changeFloorButton.pos().x(), value + 15)

        self.changeFloorButton.raise_()

    def updateHorizontalHeaderPosition(self, value):
        self.changeFloorButton.move(value + 15, self.changeFloorButton.pos().y())

        self.changeFloorButton.raise_()

    def hideStore(self):
        self.changeFloorButton.hide()

    def showIcon(self):
        self.storeIcon.show()

    def hideIcon(self):
        self.storeIcon.hide()

    def configCategories(self):
        self.goBackStore.hide()

    def configSpace(self):
        self.changeFloorButton.hide()
        self.goBackStore.show()

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
    
    # Hide and show objects
    def hideMainButtons(self):
        self.addStoreButton.hide()
        self.goHome.show()
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
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
