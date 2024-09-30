from PyQt5.QtWidgets import QLabel, QPushButton

from utils.functions.shelfFunctions import updateShelfPosition

from utils.language import Language
from utils.inputBool import InputBool
from utils.inputNumber import InputNumber

from components.space import Space

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES, DEFAULT_SPACE_MARGIN

class Shelf(QLabel):
    def __init__(self, name, posx, posy, mainWindow, parent = None):
        super().__init__(parent)
        self.setGeometry(posx, posy, WINDOW_WIDTH, WINDOW_HEIGHT)

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
            self.delStore.setGeometry(75, 10, 50, 20)
            self.delStore.clicked.connect(self.delShelf)

            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 700, 3)
            self.separator.setStyleSheet("background-color: black;")

        # Config shelf
        self.configNewShelveLabel = QLabel(Language.get("shelf_question_1"), self)
        self.configNewShelveLabel.setGeometry(0, 35, 200, 35)

        self.configNewShelveInput = InputNumber(1, True, self)
        self.configNewShelveInput.setGeometry(390, 25, 175, 50)

        self.sidesNewShelf = QLabel(Language.get("shelf_question_2"), self)
        self.sidesNewShelf.setGeometry(0, 65, 300, 35)

        self.sidesNewShelfInput = InputBool(Language.get("yes"), Language.get("no"), self)
        self.sidesNewShelfInput.setGeometry(390, 60, 175, 50)

        self.configFloorsShelfLabel = QLabel(Language.get("shelf_question_4"), self)
        self.configFloorsShelfLabel.setGeometry(0, 95, 200, 35)

        self.configFloorsShelfInput = InputNumber(1, True, self)
        self.configFloorsShelfInput.setGeometry(390, 95, 175, 50)

    def hideForm(self):
        self.hide()

    def delShelf(self):
        shelfToDelete = 0
        
        for index, shelf in enumerate(SHELVES):
            try:
                if shelf.delStore and self.sender() == shelf.delStore:
                    shelfToDelete = index
                    break
            except AttributeError:
                continue
        
        SHELVES[shelfToDelete].hide()
        del SHELVES[shelfToDelete]

        self.WINDOW.resizeHeightScroll()
        updateShelfPosition()

    def showForm(self):
        self.show()

    def saveInfo(self):
        self.spaces = self.configNewShelveInput.getNum()
        self.floors = self.configFloorsShelfInput.getNum()
        self.double_shelf = self.sidesNewShelfInput.getValue()

class ShelfInfo():
    def __init__(self, posx, posy, shelf, store, shelfNumber = 1, parent = None):
        self.initVariables(posx, shelf, store, shelfNumber)
        self.initUI(posx, posy, parent)
        self.initEvents()
    
    def initVariables(self, posx, shelf, store, shelfNumber):
        self.spaces = []
        self.posx = posx
        self.STORE = store
        self.floors = shelf.floors
        self.actualNumber = shelfNumber
        self.spacesLength = shelf.spaces
        self.double_shelf = shelf.double_shelf

    def initUI(self, posx, posy, parent):
        self.shelfNumber = QLabel(Language.get("shelf") + str(self.actualNumber) + ":", parent)
        self.shelfNumber.setGeometry(int(WINDOW_WIDTH / 2 - 25), posy - 25, 100, 25)
        self.shelfNumber.hide()

        for actualFloor in range(self.STORE.floor):
            times5 = 0

            if self.double_shelf:
                mod = self.spacesLength % 2
                sideSpaces = (self.spacesLength / 2).__trunc__()

                for index in range(sideSpaces):
                    if (index + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent, False, False, times5))

                for index in range(sideSpaces):
                    self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy + DEFAULT_SPACE_MARGIN, actualFloor + 1, self.floors, self.STORE, parent))
                
                if mod > 0:
                    if (sideSpaces + 1) % 5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.STORE, parent, True))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * sideSpaces), posy, actualFloor + 1, self.floors, self.STORE, parent, True, False, times5))
            else:
                for index in range(self.spacesLength):
                    mod5 = (index + 1) % 5

                    if mod5 != 0:
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent))
                    else:
                        times5 += 1
                        self.spaces.append(Space(posx + (DEFAULT_SPACE_MARGIN * index), posy, actualFloor + 1, self.floors, self.STORE, parent, False, False, times5))

    def initEvents(self):
        self.STORE.WINDOW.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalInfoPosition)

    def updateHorizontalInfoPosition(self, value):
        self.shelfNumber.move(value + int(WINDOW_WIDTH / 2 - self.shelfNumber.width() / 2), self.shelfNumber.pos().y())

    def changeFloor(self, number):
        self.shelfNumber.show()

        for space in self.spaces:
            space.showFloor(number)

    def hideSpaces(self):
        self.shelfNumber.hide()

        for space in self.spaces:
            if isinstance(space, Space):
                space.hideSpace()
