from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton

from constants import PRODUCTS_INFO

from utils.language import Language
from utils.product import Product

class SpaceProduct(QLabel):
    def __init__(self, parent):
        self.initVariables()
        self.initUI(parent)

    def initVariables(self):
        self.productSelector = None
        self.actualProduct = {}
        self.amountProducts = 0

    def initUI(self, parent):
        self.productLabel = QLabel(Language.get("product"), parent)
        self.productLabel.setGeometry(160, 65, 100, 25)
        self.productLabel.hide()

        self.productSelector = QComboBox(parent)
        self.productSelector.setGeometry(210, 65, 100, 25)
        self.productSelector.hide()

        self.addProduct = QPushButton(Language.get("add_product"), parent)
        self.addProduct.setGeometry(320, 65, 100, 25)
        self.addProduct.hide()

        for prod in PRODUCTS_INFO:
            self.productSelector.addItem(prod.name)
    
    def hide(self):
        self.addProduct.hide()
        self.productLabel.hide()
        self.productSelector.hide()
    
    def show(self):
        self.addProduct.show()
        self.productLabel.show()

        if PRODUCTS_INFO.__len__() >= 1:
            self.productSelector.show()

    def setProduct(self, id, amount):
        self.actualProduct = Product.get(id)
        self.amountProducts = amount
    
    def createProduct(self, id, info, amount):
        Product.set(id, info)

        self.actualProduct = info
        self.amountProducts = amount