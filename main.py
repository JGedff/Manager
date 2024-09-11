# CONNECT FIRST SPACE WITH THE OTHER STORES

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea

from components.space import Space
from components.shelf import Shelf
from components.store import Store

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, SHELVES, DEFAULT_SHELF_PREFIX, DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, DEFAULT_SHELF_MARGIN, DEFAULT_SPACE_MARGIN, STORES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

        SHELVES.append(Shelf(DEFAULT_SHELF_PREFIX + str(SHELVES.__len__() + 1), DEFAULT_SHELF_WIDTH, DEFAULT_SHELF_HEIGHT, self, self.widget))

        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeScroll()

    def initUI(self, parent):
        # Create main buttons
        self.addStoreButton = QPushButton("+ Add store", parent)
        self.addStoreButton.setGeometry(WINDOW_WIDTH - 125, WINDOW_HEIGHT - 75, 100, 50)

        # New store form
        self.newStoreLabel = QLabel("", parent)
        self.newStoreLabel.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.newStoreLabel.setStyleSheet("background-color: #dddddd;")
        self.newStoreLabel.hide()

        # Config new store
        self.newStoreNameLabel = QLabel("Name of the store:", parent)
        self.newStoreNameLabel.setGeometry(400, 20, 100, 35)
        self.newStoreNameLabel.hide()
        
        self.newStoreNameEdit = QLineEdit(parent)
        self.newStoreNameEdit.setGeometry(800, 20, 300, 35)
        self.newStoreNameEdit.setPlaceholderText("Store 1")
        self.newStoreNameEdit.hide()

        # Add new shelf
        self.createButtonsBackground = QLabel("", parent)
        self.createButtonsBackground.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.createButtonsBackground.setStyleSheet("background-color: #dddddd;")
        self.createButtonsBackground.hide()

        self.createShelfButton = QPushButton("+ Add shelf", parent)
        self.createShelfButton.setGeometry(830, WINDOW_HEIGHT - 62, 100, 50)
        self.createShelfButton.hide()

        # Create store
        self.createStoreButton = QPushButton("+ Create store", parent)
        self.createStoreButton.setGeometry(1000, WINDOW_HEIGHT - 62, 100, 50)
        self.createStoreButton.hide()

        # Go home        
        self.goBackHomeButton = QPushButton("← Go back", parent)
        self.goBackHomeButton.setGeometry(1300, 10, 100, 50)
        self.goBackHomeButton.hide()

        # Show edit categories button
        store = Store("", "", 0, 0, self, parent)
        store.hideIcon()
        
        STORES.append(store)

        self.categorySpace = Space(0, 0, 0, 0, store, parent, False, True)
        self.categorySpace.STORE.hideStore()
        self.categorySpace.STORE.hideIcon()
        self.categorySpace.hideSpace()

        self.editCategories = QPushButton("Edit categories ⚙️", parent)
        self.editCategories.setGeometry(1316, 610, 100, 30)

        if STORES.__len__() > 1:
            self.editCategories.show()
        else:
            self.editCategories.hide()

        for i, instance in enumerate(STORES):
            if i != 0:
                if isinstance(instance, Store):
                    instance.showIcon()

    def resizeScroll(self, height = 0):
        if height == 0:
            if SHELVES.__len__() > 0 and SHELVES[SHELVES.__len__() - 1].pos().y() + 250 > WINDOW_HEIGHT:
                self.widget.resize(WINDOW_WIDTH - 20, SHELVES[SHELVES.__len__() - 1].pos().y() + 250)
            else:
                self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

            self.createButtonsBackground.raise_()
            self.createShelfButton.raise_()
            self.createStoreButton.raise_()

            for index, obj in enumerate(SHELVES):
                if isinstance(obj, Shelf):
                    obj.setGeometry(obj.pos().x(), (DEFAULT_SHELF_MARGIN * (index + 1)), obj.width(), obj.height())
        else:
            width = WINDOW_WIDTH - 5
            aux = height + 175

            if aux > WINDOW_HEIGHT - 5:
                width -= 15

            self.widget.resize(width, aux)

    def initEvents(self):
        self.addStoreButton.clicked.connect(self.addStore)
        self.goBackHomeButton.clicked.connect(self.reOpenHome)
        self.createShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.createStore)
        self.editCategories.clicked.connect(self.configCategories)

        self.scroll.verticalScrollBar().valueChanged.connect(self.updateHeaderPosition)
    
    def updateHeaderPosition(self, value):
        self.newStoreLabel.move(self.newStoreLabel.pos().x(), value)
        self.editCategories.move(self.editCategories.pos().x(), value + 610)
        self.goBackHomeButton.move(self.goBackHomeButton.pos().x(), value + 10)
        self.newStoreNameEdit.move(self.newStoreNameEdit.pos().x(), value + 20)
        self.newStoreNameLabel.move(self.newStoreNameLabel.pos().x(), value + 20)
        self.addStoreButton.move(self.addStoreButton.pos().x(), value + (WINDOW_HEIGHT - 75))
        self.createStoreButton.move(self.createStoreButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.createShelfButton.move(self.createShelfButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.createButtonsBackground.move(self.createButtonsBackground.pos().x(), value + (WINDOW_HEIGHT - 75))

        self.newStoreLabel.raise_()
        self.createButtonsBackground.raise_()
        self.addStoreButton.raise_()
        self.editCategories.raise_()
        self.goBackHomeButton.raise_()
        self.newStoreNameEdit.raise_()
        self.createShelfButton.raise_()
        self.createStoreButton.raise_()
        self.newStoreNameLabel.raise_()

    def addStore(self):
        self.newStoreLabel.show()
        self.createButtonsBackground.show()
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
        self.categorySpace.category.cancelAddCategory()
        self.newStoreLabel.hide()
        self.createButtonsBackground.hide()
        self.newStoreNameEdit.hide()
        self.goBackHomeButton.hide()
        self.newStoreNameLabel.hide()
        self.createStoreButton.hide()
        self.createShelfButton.hide()
        self.addStoreButton.show()

        if STORES.__len__() > 1:
            self.editCategories.show()
        else:
            self.editCategories.hide()

        for i, instance in enumerate(STORES):
            if i != 0:
                if isinstance(instance, Store):
                    instance.hideStore()
                    instance.showIcon()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.hideForm()

        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

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
        self.newStoreNameEdit.setPlaceholderText("Store " + str(STORES.__len__() - 1))

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                shelf.saveInfo()
            
        posx = 25
        posy = 25
        
        for index, _ in enumerate(STORES):
            if index != 0:
                posx += 170

                if posx + 170 >= WINDOW_WIDTH:
                    posx = 25
                    posy += 170

        if val == "":
            STORES.append(Store("Store " + str(STORES.__len__()), "img/magazine.png", posx, posy, self, self.widget))
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