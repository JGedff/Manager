import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea

from utils.language import Language

from components.space import Space
from components.shelf import Shelf
from components.store import Store
from components.languageChanger import LanguageChanger

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, SHELVES, STORES, DEFAULT_IMAGE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initVariables()
        self.initUI(self.widget)
        self.initEvents()
        
        self.setCentralWidget(self.scroll)
        self.resizeHeightScroll()

    def initVariables(self):
        # Window config
        self.setWindowTitle(Language.get("window_title"))
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add scroll to window
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        self.scroll.setWidget(self.widget)

    def initUI(self, parent):
        # Main buttons
        self.languageChanger = LanguageChanger(self, parent)

        self.goHome = QPushButton(Language.get(""), parent)
        self.goHome.setGeometry(1300, 10, 100, 50)
        self.goHome.hide()

        self.addStoreButton = QPushButton(Language.get("add_store"), parent)
        self.addStoreButton.setGeometry(WINDOW_WIDTH - 135, WINDOW_HEIGHT - 75, 110, 50)

        self.editCategories = QPushButton(Language.get("edit_categories"), parent)
        self.editCategories.setGeometry(WINDOW_WIDTH - 135, 610, 110, 30)

        # Header Form
        self.headerFormBackground = QLabel("", parent)
        self.headerFormBackground.setGeometry(0, 0, WINDOW_WIDTH, 75)
        self.headerFormBackground.setStyleSheet("background-color: #dddddd;")
        self.headerFormBackground.hide()

        self.storeNameLabel = QLabel(Language.get("name_store"), parent)
        self.storeNameLabel.setGeometry(400, 20, 100, 35)
        self.storeNameLabel.hide()
        
        self.storeNameInput = QLineEdit(parent)
        self.storeNameInput.setGeometry(800, 20, 300, 35)
        self.storeNameInput.setPlaceholderText(Language.get("store") + str(1))
        self.storeNameInput.hide()

        # Footer form
        self.footerFormBackground = QLabel("", parent)
        self.footerFormBackground.setGeometry(0, WINDOW_HEIGHT - 75, WINDOW_WIDTH, 75)
        self.footerFormBackground.setStyleSheet("background-color: #dddddd;")
        self.footerFormBackground.hide()

        self.addShelfButton = QPushButton(Language.get("add_shelf"), parent)
        self.addShelfButton.setGeometry(830, WINDOW_HEIGHT - 62, 100, 50)
        self.addShelfButton.hide()

        self.createStoreButton = QPushButton(Language.get("create_store"), parent)
        self.createStoreButton.setGeometry(1000, WINDOW_HEIGHT - 62, 100, 50)
        self.createStoreButton.hide()

        # This is to make the manage category button work
        store = Store("", "", 0, 0, self, parent)
        store.hideIcon()
        
        STORES.append(store)

        self.configCategory = Space(0, 0, 0, 0, store, parent, False, True)
        self.configCategory.STORE.hideStore()
        self.configCategory.STORE.hideIcon()
        self.configCategory.hideSpace()

        # Show all stores
        for i, instance in enumerate(STORES):
            if i != 0:
                if isinstance(instance, Store):
                    instance.showIcon()

    def initEvents(self):
        # Click buttons
        self.goHome.clicked.connect(self.reOpenHome)
        self.addStoreButton.clicked.connect(self.addStore)
        self.addShelfButton.clicked.connect(self.createShelf)
        self.createStoreButton.clicked.connect(self.saveStoreInfo)
        self.editCategories.clicked.connect(self.configCategories)

        # Do scroll
        self.scroll.verticalScrollBar().valueChanged.connect(self.updateVerticalHeaderPosition)
        self.scroll.horizontalScrollBar().valueChanged.connect(self.updateHorizontalHeaderPosition)
    
    # Scroll functions
    def updateVerticalHeaderPosition(self, value):
        self.goHome.move(self.goHome.pos().x(), value + 10)
        self.editCategories.move(self.editCategories.pos().x(), value + 610)
        self.storeNameInput.move(self.storeNameInput.pos().x(), value + 20)
        self.storeNameLabel.move(self.storeNameLabel.pos().x(), value + 20)
        self.headerFormBackground.move(self.headerFormBackground.pos().x(), value)
        self.addStoreButton.move(self.addStoreButton.pos().x(), value + (WINDOW_HEIGHT - 75))
        self.addShelfButton.move(self.addShelfButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.createStoreButton.move(self.createStoreButton.pos().x(), value + (WINDOW_HEIGHT - 62))
        self.languageChanger.move(self.languageChanger.pos().x() + 15, value + (WINDOW_HEIGHT - 50))
        self.footerFormBackground.move(self.footerFormBackground.pos().x(), value + (WINDOW_HEIGHT - 75))

        self.raiseShelfHeaderForm()

    def updateHorizontalHeaderPosition(self, value):
        self.goHome.move(value + 1300, self.goHome.pos().y())

    # Resize scroll functions
    def resizeHeightScroll(self, height = 0):
        if height == 0:
            if SHELVES.__len__() > 0 and SHELVES[SHELVES.__len__() - 1].pos().y() + 250 > WINDOW_HEIGHT:
                self.widget.resize(WINDOW_WIDTH - 20, SHELVES[SHELVES.__len__() - 1].pos().y() + 250)
            else:
                self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

            self.raiseShelfFooterForm()
        else:
            width = WINDOW_WIDTH - 5
            aux = height + 175

            if aux > WINDOW_HEIGHT - 5:
                width -= 15

            self.widget.resize(width, aux)

    def resizeWidthScroll(self, width = WINDOW_WIDTH):
        if width < WINDOW_WIDTH:
            self.widget.resize(self.widget.width(), self.widget.height())
        else:
            self.widget.resize(width + 125, self.widget.height())

    def resizeMain(self):
        if STORES.__len__() < 26:
            self.widget.resize(WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
        else:
            self.widget.resize(WINDOW_WIDTH - 20, STORES[STORES.__len__() - 1].storeIcon.pos().y() + 290)

    # UI functions
    def reOpenHome(self):
        self.configCategory.category.cancelAddCategory()
        self.configCategory.category.hideUI()
        
        self.showMainButtons()
        self.hideAddStoreForm()
        self.raiseMainButtons()

        for i, instance in enumerate(STORES):
            if i != 0:
                if isinstance(instance, Store):
                    instance.hideStore()
                    instance.showIcon()

        for i in SHELVES:
            if isinstance(i, Shelf):
                i.hideForm()

        self.resizeMain()

    def addStore(self):
        self.showAddStoreForm()
        self.resizeHeightScroll()
        
        for i in SHELVES:
            if isinstance(i, Shelf):
                i.showForm()

        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()

        self.goHome.show()
        self.goHome.raise_()
        self.editCategories.hide()

    def createShelf(self):
        newShelf = Shelf(Language.get("shelf") + str(SHELVES.__len__() + 1), SHELVES[SHELVES.__len__() - 1].pos().x(), SHELVES[SHELVES.__len__() - 1].pos().y() + 150, self, self.widget)
        newShelf.showForm()
        
        SHELVES.append(newShelf)

        self.resizeHeightScroll()

    def saveStoreInfo(self):
        storeName = self.storeNameInput.text().strip()
        self.storeNameInput.setText("")
        self.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))

        for shelf in SHELVES:
            if isinstance(shelf, Shelf):
                shelf.saveInfo()
            
        self.createStore(storeName)
        
        self.reOpenHome()
        self.goHome.raise_()
    
    def configCategories(self):
        for i in STORES:
            if isinstance(i, Store):
                i.hideIcon()

        self.hideMainButtons()
        self.configCategory.configSpace()
        self.configCategory.openSpaceConfig.hide()

    # Functions
    def createStore(self, nameStore):
        posx = 25
        posy = 25
        
        for index, _ in enumerate(STORES):
            if index != 0:
                posx += 170

                if posx + 170 >= WINDOW_WIDTH:
                    posx = 25
                    posy += 170

        if nameStore == "":
            STORES.append(Store(Language.get("store") + str(STORES.__len__()), DEFAULT_IMAGE, posx, posy, self, self.widget))
        else:
            STORES.append(Store(nameStore, DEFAULT_IMAGE, posx, posy, self, self.widget))

    # Show objects
    def showAddStoreForm(self):
        self.headerFormBackground.show()
        self.footerFormBackground.show()
        self.createStoreButton.show()
        self.storeNameInput.show()
        self.storeNameLabel.show()
        self.addShelfButton.show()

    def showMainButtons(self):
        self.languageChanger.show()
        self.editCategories.show()
        self.addStoreButton.show()

    # Hide objects
    def hideAddStoreForm(self):
        self.headerFormBackground.hide()
        self.footerFormBackground.hide()
        self.createStoreButton.hide()
        self.storeNameInput.hide()
        self.storeNameLabel.hide()
        self.addShelfButton.hide()
        self.goHome.hide()
    
    # Hide and show objects
    def hideMainButtons(self):
        self.addStoreButton.hide()
        self.goHome.show()
        self.editCategories.hide()
        self.languageChanger.hide()

    # Raise objects
    def raiseShelfFooterForm(self):
        self.footerFormBackground.raise_()
        self.createStoreButton.raise_()
        self.addShelfButton.raise_()

    def raiseShelfHeaderForm(self):
        self.headerFormBackground.raise_()
        self.storeNameInput.raise_()
        self.storeNameLabel.raise_()
        self.goHome.raise_()
    
    def raiseMainButtons(self):
        self.languageChanger.raise_()
        self.addStoreButton.raise_()
        self.editCategories.raise_()

class main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()