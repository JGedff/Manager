from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from constants import PRODUCTS_INFO

from utils.category import Category
from utils.language import Language
from utils.product import Product

class SpaceProduct(QLabel):
    def __init__(self, category, parent):
        super().__init__(parent)

        self.initVariables(category)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, category):
        self.amountProducts = 0
        self.category = category
        self.actualProduct = None

    def initUI(self, parent):
        self.productLabel = QLabel(Language.get("product"), parent)
        self.productLabel.setGeometry(160, 65, 100, 25)

        self.productSelector = QComboBox(parent)
        self.productSelector.setGeometry(210, 65, 125, 25)

        self.addProduct = QPushButton(Language.get("add_product"), parent)
        self.addProduct.setGeometry(345, 65, 125, 25)

        self.cancelAddProduct = QPushButton(Language.get("cancel"), parent)
        self.cancelAddProduct.setGeometry(345, 100, 125, 25)
        self.cancelAddProduct.hide()

        self.productSelector.addItem(Language.get("no_product"))

        for prod in PRODUCTS_INFO:
            self.productSelector.addItem(prod.name)
    
    def initEvents(self):
        self.productSelector.currentTextChanged.connect(self.changeProduct)
        self.addProduct.clicked.connect(self.openCreateProduct)
        self.cancelAddProduct.clicked.connect(self.closeCreateProduct)

    def changeProduct(self, productName):
        if productName == Language.get("no_product"):
            self.actualProduct = None
        else:
            self.actualProduct = Product.getByName(self.productSelector.currentText())

    def openCreateProduct(self):
        self.cancelAddProduct.show()

    def closeCreateProduct(self):
        self.cancelAddProduct.hide()

    def categoryChanged(self):
        if Category.isProductCategory(self.category.name):
            self.addProduct.show()
            self.productLabel.show()
            self.productSelector.show()
        else:
            self.addProduct.hide()
            self.productLabel.hide()
            self.productSelector.hide()


    def hide(self):
        self.addProduct.hide()
        self.productLabel.hide()
        self.productSelector.hide()
    
    def show(self):
        if Category.isProductCategory(self.category.name):
            self.addProduct.show()
            self.productLabel.show()
            self.productSelector.show()