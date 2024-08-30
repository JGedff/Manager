from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

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

    def updateWindow(self):
        self.WINDOW.resizeScroll()
    
    def setupStore(self, mainWindow, parent):
        self.WINDOW = mainWindow
        self.shelves = []
        self.floor = self.getMaxFloor()

        for index, i in enumerate(SHELVES):
            if isinstance(i, Shelf):
                i.hideForm()
                self.shelves.append(ShelfInfo(25, 50 + (185 * index), i, self, self.WINDOW, parent))
        
        SHELVES.clear()
        SHELVES.append(Shelf("Shelf " + str(SHELVES.__len__() + 1), 400, 130, mainWindow, parent))

    def getMaxFloor(self):
        maxFloor = 1

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                if maxFloor < shelf.floors:
                    maxFloor = shelf.floors
        
        return maxFloor

    def initUI(self, name, image, posx, posy, parent):
        self.goBackStore = QPushButton("← Go back", parent)
        self.goBackStore.setGeometry(1300, 15, 100, 50)
        self.goBackStore.hide()

        self.storeIcon = ImageButton(name, image, parent)
        self.storeIcon.setGeometry(posx, posy, 150, 150)

        self.changeFloorButton = QComboBox(parent)
        self.changeFloorButton.setGeometry(25, 15, 125, 25)

        for index in range(self.floor):
            self.changeFloorButton.addItem("Floor: " + str(index + 1))

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()

    def initEvents(self):
        self.storeIcon.clicked.connect(self.openStore)
        self.goBackStore.clicked.connect(self.openStore)
        self.changeFloorButton.currentTextChanged.connect(self.changeFloor)

    def changeFloor(self):
        for shelf in self.shelves:
            shelf.changeFloor(int(self.changeFloorButton.currentText().split(' ')[1]))

    def openStore(self):
        self.WINDOW.openStore()
        self.goBackStore.hide()

        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()
            
        self.showStore()
        self.changeFloor()

    def showStore(self):
        self.changeFloorButton.show()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.showSpaces()

    def hideStore(self):
        self.changeFloorButton.hide()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()

    def showIcon(self):
        self.storeIcon.show()

    def hideIcon(self):
        self.storeIcon.hide()

    def configSpace(self):
        self.changeFloorButton.hide()
        self.goBackStore.show()

        for shelf in self.shelves:
            if isinstance(shelf, ShelfInfo):
                shelf.hideSpaces()

    def configCategories(self):
        self.goBackStore.hide()