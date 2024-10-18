from PyQt5.QtWidgets import QLabel, QPushButton

from utils.functions.shelfFunctions import updateShelfPosition

from utils.language import Language
from utils.inputBool import InputBool
from utils.inputNumber import InputNumber

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES_FORMS

class Shelf(QLabel):
    @staticmethod
    def createShelf(parent):
        length = SHELVES_FORMS.__len__()

        if length > 0:
            newShelf = Shelf(Language.get("shelf") + str(length + 1), SHELVES_FORMS[length - 1].pos().x(), SHELVES_FORMS[length - 1].pos().y() + 150, parent)
        else:
            newShelf = Shelf(Language.get("shelf") + str(length + 1), 400, 100, parent)
        
        newShelf.showForm()

        SHELVES_FORMS.append(newShelf)

    @staticmethod
    def hideAllForms():
        for shelf in SHELVES_FORMS:
            shelf.hideForm()

    @staticmethod
    def showAllForms():    
        for i in SHELVES_FORMS:
            i.showForm()

    def __init__(self, name, posx, posy, parent = None):
        super().__init__(parent)
        
        self.setGeometry(posx, posy, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.initVariables()
        self.initUI(name)
        self.hideForm()
    
    def initVariables(self):
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
        if SHELVES_FORMS.__len__() + 1 > 1:
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
        
        for index, shelf in enumerate(SHELVES_FORMS):
            try:
                if self.sender() == shelf.delShelfButton:
                    shelfToDelete = index
                    break
            except AttributeError:
                continue
        
        SHELVES_FORMS[shelfToDelete].hide()
        del SHELVES_FORMS[shelfToDelete]

        updateShelfPosition()

    def showForm(self):
        self.show()

    def saveInfo(self):
        self.spaces = self.inputSpaces.getNum()
        self.floors = self.shelfFloorsInput.getNum()
        self.double_shelf = self.doubleShelfInput.getValue()

