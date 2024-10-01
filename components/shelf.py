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
        # Config shelf
        self.shelfLabel = QLabel(name, self)
        self.shelfLabel.setGeometry(0, 0, 100, 35)

        self.inputSpacesLabel = QLabel(Language.get("shelf_question_1"), self)
        self.inputSpacesLabel.setGeometry(0, 35, 200, 35)

        self.inputSpaces = InputNumber(1, True, self)
        self.inputSpaces.setGeometry(390, 25, 175, 50)

        self.doubleShelfLabel = QLabel(Language.get("shelf_question_2"), self)
        self.doubleShelfLabel.setGeometry(0, 65, 300, 35)

        self.doubleShelfInput = InputBool(Language.get("yes"), Language.get("no"), self)
        self.doubleShelfInput.setGeometry(390, 60, 175, 50)

        self.shelfFloorsLabel = QLabel(Language.get("shelf_question_4"), self)
        self.shelfFloorsLabel.setGeometry(0, 95, 200, 35)

        self.shelfFloorsInput = InputNumber(1, True, self)
        self.shelfFloorsInput.setGeometry(390, 95, 175, 50)

        # Option to delete shelf if there is more than one shelf
        if SHELVES.__len__() + 1 > 1:
            self.delShelfButton = QPushButton("🗑️", self)
            self.delShelfButton.setGeometry(75, 10, 50, 20)
            self.delShelfButton.clicked.connect(self.delShelf)

            self.separator = QLabel(self)
            self.separator.setGeometry(0, 0, 700, 3)
            self.separator.setStyleSheet("background-color: black;")

    def hideForm(self):
        self.hide()

    def delShelf(self):
        shelfToDelete = 0
        
        for index, shelf in enumerate(SHELVES):
            try:
                if self.sender() == shelf.delShelfButton:
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
        self.spaces = self.inputSpaces.getNum()
        self.floors = self.shelfFloorsInput.getNum()
        self.double_shelf = self.doubleShelfInput.getValue()

class ShelfInfo():
    def __init__(self, posx, posy, floors, spaces, double_shelf, store, shelfNumber = 1, parent = None):
        self.initVariables(posx, floors, spaces, double_shelf, store, shelfNumber)
        self.initUI(posx, posy, parent)
        self.initEvents()
    
    def initVariables(self, posx, floors, spaces, double_shelf, store, shelfNumber):
        self.spaces = []
        self.posx = posx
        self.STORE = store
        self.floors = floors
        self.actualNumber = shelfNumber
        self.spacesLength = spaces
        self.double_shelf = double_shelf

    def initUI(self, posx, posy, parent):
        self.shelfNumber = QLabel(Language.get("shelf") + str(self.actualNumber) + ":", parent)
        self.shelfNumber.setGeometry(int(WINDOW_WIDTH / 2 - self.shelfNumber.width() / 2), posy - 25, 100, 25)
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
