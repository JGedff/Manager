from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from utils.language import Language
from utils.imageButton import ImageButton

from components.shelf import Shelf, ShelfInfo

from constants import SHELVES, STORES

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
                self.shelves.append(ShelfInfo(25, 50 + (185 * index), i, self, (index + 1), parent))
        
        SHELVES.clear()
        SHELVES.append(Shelf(Language.get("shelf") + str(SHELVES.__len__() + 1), 400, 100, mainWindow, parent))

    def getMaxFloor(self):
        maxFloor = 1

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                if maxFloor < shelf.floors:
                    maxFloor = shelf.floors
        
        return maxFloor

    def updateWindow(self):
        self.WINDOW.resizeHeightScroll()
        self.WINDOW.resizeWidthScroll()

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
        self.WINDOW.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.WINDOW.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)

    def openStore(self):
        self.WINDOW.hideMainButtons()
        self.goBackStore.hide()

        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()
            
        self.changeFloorButton.show()
        self.changeFloor(self.changeFloorButton.currentText())

        maxPosY = 0
        maxPosX = 0

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                if shelf.spaces[shelf.spaces.__len__() - 1].pos().y() > maxPosY:
                    maxPosY = shelf.spaces[shelf.spaces.__len__() - 1].pos().y()

                if shelf.spaces[shelf.spaces.__len__() - 1].pos().x() > maxPosX:
                    maxPosX = shelf.spaces[shelf.spaces.__len__() - 1].pos().x()
    
        self.WINDOW.resizeHeightScroll(maxPosY)
        self.WINDOW.resizeWidthScroll(maxPosX)

    def changeFloor(self, floor):
        if floor.__len__() >= 1:
            for shelf in self.shelves:
                shelf.changeFloor(int(self.changeFloorButton.currentText().split(' ')[1]))

    def updateVerticalHeaderPosition(self, value):
        self.changeFloorButton.move(self.changeFloorButton.pos().x(), value + 15)

        self.changeFloorButton.raise_()

    def updateHorizontalHeaderPosition(self, value):
        self.changeFloorButton.move(value + 15, self.changeFloorButton.pos().y())

        self.changeFloorButton.raise_()

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
        self.WINDOW.goHome.hide()
        self.changeFloorButton.hide()
        self.goBackStore.show()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()