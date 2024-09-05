import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea

from components.space import Space
from components.shelf import Shelf
from components.store import Store

from constants import WINDOW_WIDTH, WINDOW_HEIGTH, WINDOW_TITLE, SHELVES, DEFAULT_SHELF_PREFIX, DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, DEFAULT_SHELF_MARGIN, STORES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGTH)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)
        self.scroll.setWidget(self.widget)

        SHELVES.append(Shelf(DEFAULT_SHELF_PREFIX + str(SHELVES.__len__() + 1), DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, self, self.widget))

        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeScroll()

    def initUI(self, parent):
        # Create main buttons
        self.addStoreButton = QPushButton("+ Add store", parent)
        self.addStoreButton.setGeometry(WINDOW_WIDTH - 125, WINDOW_HEIGTH - 75, 100, 50)

        # New store form
        self.newStoreLabel = QLabel("New store", parent)
        self.newStoreLabel.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.newStoreLabel.setStyleSheet("background-color: #dddddd;")
        self.newStoreLabel.hide()

        # Config new store
        self.newStoreNameLabel = QLabel("Name of the store:", parent)
        self.newStoreNameLabel.setGeometry(400, 100, 100, 35)
        self.newStoreNameLabel.hide()
        
        self.newStoreNameEdit = QLineEdit(parent)
        self.newStoreNameEdit.setGeometry(800, 100, 300, 35)
        self.newStoreNameEdit.setPlaceholderText("Store 1")
        self.newStoreNameEdit.hide()

        # Add new shelf
        self.createShelfButton = QPushButton("+ Add shelf", parent)
        self.createShelfButton.setGeometry(830, 340, 100, 35)
        self.createShelfButton.hide()

        # Create store
        self.createStoreButton = QPushButton("+ Create store", parent)
        self.createStoreButton.setGeometry(830, 390, 100, 35)
        self.createStoreButton.hide()

        # Go home        
        self.goBackHomeButton = QPushButton("← Go back", parent)
        self.goBackHomeButton.setGeometry(1300, 15, 100, 50)
        self.goBackHomeButton.hide()

        # Show edit categories button
        self.categorySpace = Space(0, 0, 0, 0, Store("", "", 0, 0, self, parent), parent, False, True)
        self.categorySpace.STORE.hideStore()
        self.categorySpace.STORE.hideIcon()
        self.categorySpace.hideSpace()

        self.editCategories = QPushButton("Edit categories ⚙️", parent)
        self.editCategories.setGeometry(1316, 610, 100, 30)

        if STORES.__len__() > 0:
            self.editCategories.show()
        else:
            self.editCategories.hide()

        for i in STORES:
            if isinstance(i, Store):
                i.showIcon()

    def resizeScroll(self):
        if SHELVES.__len__() > 0 and SHELVES[SHELVES.__len__() - 1].pos().y() + 250 > WINDOW_HEIGTH:
            self.widget.resize(WINDOW_WIDTH - 20, SHELVES[SHELVES.__len__() - 1].pos().y() + 250)
        else:
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)

        self.createShelfButton.setGeometry(SHELVES[SHELVES.__len__() - 1].pos().x(), SHELVES[SHELVES.__len__() - 1].pos().y() + DEFAULT_SHELF_MARGIN, self.createShelfButton.width(), self.createShelfButton.height())
        self.createShelfButton.raise_()

        self.createStoreButton.setGeometry(SHELVES[SHELVES.__len__() - 1].pos().x() + DEFAULT_SHELF_WIDTH, SHELVES[SHELVES.__len__() - 1].pos().y() + DEFAULT_SHELF_MARGIN, self.createStoreButton.width(), self.createStoreButton.height())
        self.createStoreButton.raise_()

        for index, obj in enumerate(SHELVES):
            if isinstance(obj, Shelf):
                obj.setGeometry(obj.pos().x(), (DEFAULT_SHELF_MARGIN * (index + 1)), obj.width(), obj.height())

    def initEvents(self):
        self.addStoreButton.clicked.connect(self.addStore)
        self.goBackHomeButton.clicked.connect(self.reOpenHome)
        self.createShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.createStore)
        self.editCategories.clicked.connect(self.configCategories)

    def addStore(self):
        self.newStoreLabel.show()
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

        # It only hides and shows the same items as when it opens a store, but here it does not open a store
        self.openStore()

        self.resizeScroll()

    def reOpenHome(self):
        self.newStoreLabel.hide()
        self.newStoreNameEdit.hide()
        self.goBackHomeButton.hide()
        self.newStoreNameLabel.hide()
        self.createStoreButton.hide()
        self.createShelfButton.hide()
        self.addStoreButton.show()

        if STORES.__len__() > 0:
            self.editCategories.show()
        else:
            self.editCategories.hide()

        for i in STORES:
            if isinstance(i, Store):
                i.hideStore()
                i.showIcon()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.hideForm()

        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGTH - 5)

        # This case is for when you open category configuration from main
        self.categorySpace.category.hideUI()

    def createShelf(self):
        SHELVES.append(Shelf(DEFAULT_SHELF_PREFIX + str(SHELVES.__len__() + 1), SHELVES[SHELVES.__len__() - 1].pos().x(), SHELVES[SHELVES.__len__() - 1].pos().y() + DEFAULT_SHELF_MARGIN, self, self.widget))

        self.resizeScroll()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.showForm()

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
    
    def configCategories(self):
        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()

        self.openStore()
        self.categorySpace.configSpace()
        self.categorySpace.openSpaceConfig.hide()

    def openStore(self):
        self.addStoreButton.hide()
        self.goBackHomeButton.show()
        self.editCategories.hide()

class main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()