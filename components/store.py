from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from utils.language import Language
from utils.imageButton import ImageButton

from components.shelf import Shelf, ShelfInfo

from constants import SHELVES, DEFAULT_SHELF_PREFIX, DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, STORES

class Store(QLabel):
    def __init__(self, name, image, posx, posy, mainWindow, parent):
        super().__init__(parent)
        
        self.setupStore(mainWindow, parent)
        self.updateWindow()

        self.initUI(name, image, posx, posy, parent)
        self.initEvents()
    
    def setupStore(self, mainWindow, parent):
        self.WINDOW = mainWindow
        self.shelves = []
        self.floor = self.getMaxFloor()

        for index, i in enumerate(SHELVES):
            if isinstance(i, Shelf):
                i.hideForm()
                self.shelves.append(ShelfInfo(25, 50 + (185 * index), i, self, parent))
        
        SHELVES.clear()
        SHELVES.append(Shelf(DEFAULT_SHELF_PREFIX + str(SHELVES.__len__() + 1), DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, mainWindow, parent))

    def getMaxFloor(self):
        maxFloor = 1

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                if maxFloor < shelf.floors:
                    maxFloor = shelf.floors
        
        return maxFloor

    def updateWindow(self):
        self.WINDOW.resizeScroll()

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
        self.WINDOW.scroll.verticalScrollBar().valueChanged.connect(self.updateHeaderPosition)

    def openStore(self):
        self.WINDOW.openStore()
        self.goBackStore.hide()

        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()
            
        self.changeFloorButton.show()
        self.changeFloor()

        maxPosY = 0

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                if shelf.spaces[shelf.spaces.__len__() - 1].pos().y() > maxPosY:
                    maxPosY = shelf.spaces[shelf.spaces.__len__() - 1].pos().y()

        self.WINDOW.resizeScroll(maxPosY)

    def changeFloor(self):
        for shelf in self.shelves:
            shelf.changeFloor(int(self.changeFloorButton.currentText().split(' ')[1]))

    def updateHeaderPosition(self, value):
        self.changeFloorButton.move(self.changeFloorButton.pos().x(), value + 15)

    def hideStore(self):
        self.changeFloorButton.hide()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()

    def showIcon(self):
        self.storeIcon.show()

    def hideIcon(self):
        self.storeIcon.hide()

    def configCategories(self):
        self.goBackStore.hide()

    def configSpace(self):
        self.WINDOW.goBackHomeButton.hide()
        self.changeFloorButton.hide()
        self.goBackStore.show()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()