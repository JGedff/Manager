import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea

from components.space import Space
from components.shelf import Shelf
from components.store import Store

from constants import WINDOW_WIDTH, WINDOW_HEIGTH, SHELVES, STORES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGTH)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)
        self.scroll.setWidget(self.widget)

        SHELVES.append(Shelf("Shelf " + str(SHELVES.__len__() + 1), 400, 130, self, self.widget))

        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeScroll()

    def resizeScroll(self):
        if SHELVES.__len__() > 0 and SHELVES[SHELVES.__len__() - 1].pos().y() + 250 > WINDOW_HEIGTH:
            self.widget.resize(WINDOW_WIDTH - 20, SHELVES[SHELVES.__len__() - 1].pos().y() + 250)
        else:
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)

        self.createShelfButton.setGeometry(SHELVES[SHELVES.__len__() - 1].pos().x(), SHELVES[SHELVES.__len__() - 1].pos().y() + 150, self.createShelfButton.width(), self.createShelfButton.height())
        self.createShelfButton.raise_()

        self.createStoreButton.setGeometry(SHELVES[SHELVES.__len__() - 1].pos().x() + 400, SHELVES[SHELVES.__len__() - 1].pos().y() + 150, self.createStoreButton.width(), self.createStoreButton.height())
        self.createStoreButton.raise_()

        for index, obj in enumerate(SHELVES):
            if isinstance(obj, Shelf):
                obj.setGeometry(obj.pos().x(), (150 * (index + 1)), obj.width(), obj.height())

    def initUI(self, parent):
        # Create main buttons
        self.addStoreButton = QPushButton("+ Add store", parent)
        self.addStoreButton.setGeometry(WINDOW_WIDTH - 125, WINDOW_HEIGTH - 75, 100, 50)

        # New store form
        self.newStoreLabel = QLabel("New store", parent)
        self.newStoreLabel.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.newStoreLabel.setStyleSheet("background-color: #dddddd;")
        self.newStoreLabel.hide()

        # Config
        self.newStoreNameLabel = QLabel("Name of the store:", parent)
        self.newStoreNameLabel.setGeometry(400, 100, 100, 35)
        self.newStoreNameLabel.hide()
        
        self.newStoreNameEdit = QLineEdit(parent)
        self.newStoreNameEdit.setGeometry(800, 100, 300, 35)
        self.newStoreNameEdit.setPlaceholderText("Store 1")
        self.newStoreNameEdit.hide()

        self.createStoreButton = QPushButton("+ Create store", parent)
        self.createStoreButton.setGeometry(830, 390, 100, 35)
        self.createStoreButton.hide()

        self.goBackHomeButton = QPushButton("← Go back", parent)
        self.goBackHomeButton.setGeometry(1300, 15, 100, 50)
        self.goBackHomeButton.hide()

        self.createShelfButton = QPushButton("+ Add shelf", parent)
        self.createShelfButton.setGeometry(830, 340, 100, 35)
        self.createShelfButton.hide()

        self.editCategories = Space(0, 0, 0, Shelf("",0,0,self,parent), Store("", "", 0, 0, self, parent), self, parent, False, True)
        self.editCategories.STORE.hideStore()
        self.editCategories.STORE.hideIcon()
        self.editCategories.hideSpace()

        if STORES.__len__() > 0:
            self.editCategories.home()

        for i in STORES:
            if isinstance(i, Store):
                i.showIcon()

    def createShelf(self):
        SHELVES.append(Shelf("Shelf " + str(SHELVES.__len__() + 1), SHELVES[SHELVES.__len__() - 1].pos().x(), SHELVES[SHELVES.__len__() - 1].pos().y() + 150, self, self.widget))

        self.resizeScroll()

        if STORES.__len__() > 0:
            self.editCategories.hideHome()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.showForm()
    
    def initEvents(self):
        self.addStoreButton.clicked.connect(self.addStore)
        self.goBackHomeButton.clicked.connect(self.reOpenHome)
        self.createShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.createStore)

    def createStore(self):
        val = self.newStoreNameEdit.text()
        self.newStoreNameEdit.setText("")
        self.newStoreNameEdit.setPlaceholderText("Store " + str(STORES.__len__() + 2))

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                shelf.saveInfo()
            
        posx = 25
        posy = 25
        
        for _ in STORES:
            posx += 170

            if posx + 170 >= WINDOW_WIDTH:
                posx = 25
                posy += 170

        if val == "":
            STORES.append(Store("Store " + str(STORES.__len__() + 1), "img/magazine.png", posx, posy, self, self.widget))
        else:
            STORES.append(Store(val, "img/magazine.png", posx, posy, self, self.widget))
        
        self.reOpenHome()
    
    def addStore(self):
        self.addStoreButton.hide()
        self.newStoreLabel.show()
        self.goBackHomeButton.show()
        self.newStoreNameEdit.show()
        self.newStoreNameLabel.show()
        self.createStoreButton.show()
        self.createShelfButton.show()
        
        for i in SHELVES:
            if isinstance(i, Shelf):
                i.showForm()

        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()

        self.resizeScroll()

    def openStore(self):
        self.addStoreButton.hide()
        self.goBackHomeButton.show()

        if STORES.__len__() > 0:
            self.editCategories.hideHome()

    def reOpenHome(self):
        self.newStoreLabel.hide()
        self.newStoreNameEdit.hide()
        self.goBackHomeButton.hide()
        self.newStoreNameLabel.hide()
        self.createStoreButton.hide()
        self.createShelfButton.hide()
        self.addStoreButton.show()

        if STORES.__len__() > 0:
            self.editCategories.home()

        for i in STORES:
            if isinstance(i, Store):
                i.hideStore()
                i.showIcon()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.hideForm()

        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)

    def configSpace(self):
        self.goBackHomeButton.hide()

        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)

class main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()