from PyQt5.QtWidgets import QLabel, QPushButton

from utils.inputBool import InputBool
from utils.inputNumber import InputNumber
from components.space import Space

from constants import WINDOW_WIDTH, WINDOW_HEIGTH, SHELVES, DEFAULT_SPACE_MARGIN

class Shelf(QLabel):
    def __init__(self, name, posx, posy, mainWindow, parent = None):
        super().__init__(parent)
        self.setGeometry(posx, posy, WINDOW_WIDTH, WINDOW_HEIGTH)

        self.initVariables(mainWindow)
        self.initUI(name)
        self.hideForm()
    
    def initVariables(self, mainWindow):
        self.WINDOW = mainWindow
        self.double_shelf = False
        self.spaces = 1
        self.floors = 1

    def initUI(self, name):
        # Init shelf
        self.configNewStoreLabel = QLabel(name, self)
        self.configNewStoreLabel.setGeometry(0, 0, 100, 35)

        # Delete shelf
        if SHELVES.__len__() + 1 > 1:
            self.delStore = QPushButton("🗑️", self)
            self.delStore.setGeometry(50, 10, 50, 20)
            self.delStore.clicked.connect(self.delShelf)

            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 700, 3)
            self.separator.setStyleSheet("background-color: black;")

        # Config shelf
        self.configNewShelveLabel = QLabel("How many spaces does the shelf have?:", self)
        self.configNewShelveLabel.setGeometry(0, 35, 200, 35)

        self.configNewShelveInput = InputNumber(1, self)
        self.configNewShelveInput.setGeometry(390, 25, 175, 50)

        self.sidesNewShelf = QLabel("Can you put products in both sides of the shelf?:", self)
        self.sidesNewShelf.setGeometry(0, 65, 300, 35)

        self.sidesNewShelfInput = InputBool("Yes", "No", self)
        self.sidesNewShelfInput.setGeometry(390, 60, 175, 50)

        self.configFloorsShelfLabel = QLabel("How many floors does the shelf have?:", self)
        self.configFloorsShelfLabel.setGeometry(0, 95, 200, 35)

        self.configFloorsShelfInput = InputNumber(1, self)
        self.configFloorsShelfInput.setGeometry(390, 95, 175, 50)

    def hideForm(self):
        self.hide()

    def delShelf(self):
        SHELVES[SHELVES.__len__() - 1].hide()
        del SHELVES[SHELVES.__len__() - 1]

        self.WINDOW.resizeScroll()

    def showForm(self):
        self.show()

    def saveInfo(self):
        self.spaces = self.configNewShelveInput.getNum()
        self.floors = self.configFloorsShelfInput.getNum()
        self.double_shelf = self.sidesNewShelfInput.getValue()

class ShelfInfo():
    def __init__(self, posx, posy, shelf, store, parent = None):
        self.initVariables(shelf, store)
        self.initUI(posx, posy, parent)
    
    def initVariables(self, shelf, store):
        self.double_shelf = shelf.double_shelf
        self.spacesLength = shelf.spaces
        self.floors = shelf.floors
        self.STORE = store
        self.spaces = []

    def initUI(self, posx, posy, parent):
        for actualFloor in range(self.STORE.floor):
            if self.double_shelf:
                mod = self.spacesLength % 2
                sideSpaces = (self.spacesLength / 2).__trunc__()
                
                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent))

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy + DEFAULT_SPACE_MARGIN, actualFloor + 1, self.floors, self.STORE, parent))

                if mod > 0:
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.STORE, parent, True))
            else:
                for index in range(self.spacesLength):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent))

    def changeFloor(self, number):
        for space in self.spaces:
            space.showFloor(number)

    def hideSpaces(self):
        for space in self.spaces:
            if isinstance(space, Space):
                space.hideSpace()
