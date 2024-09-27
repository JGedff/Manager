from PyQt5.QtWidgets import QLabel, QComboBox

from utils.language import Language

from constants import WINDOW_HEIGHT, STORES, SHELVES, PRODUCTS_INFO

class LanguageChanger(QLabel):
    def __init__(self, window, parent):
        super().__init__(parent)

        self.initVariables(window)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, window):
        self.WINDOW = window

    def initUI(self,parent):
        self.changer = QComboBox(parent)
        self.changer.addItem("English")
        self.changer.addItem("Español")
        self.changer.addItem("Català")
        self.changer.setGeometry(15, WINDOW_HEIGHT - 50, 100, 25)
    
    def initEvents(self):
        self.changer.currentTextChanged.connect(self.changeLang)

    def changeLang(self, language):
        Language.changeTo(language)
        self.updateUI()

    def updateUI(self):
        # Window
        self.WINDOW.setWindowTitle(Language.get("window_title"))
        self.WINDOW.addStoreButton.setText(Language.get("add_store"))
        self.WINDOW.newStoreNameLabel.setText(Language.get("name_store"))
        self.WINDOW.newStoreNameEdit.setPlaceholderText(Language.get("store") + str(STORES.__len__() - 1))
        self.WINDOW.createShelfButton.setText(Language.get("add_shelf"))
        self.WINDOW.createStoreButton.setText(Language.get("create_store"))
        self.WINDOW.goBackHomeButton.setText(Language.get("go_back"))
        self.WINDOW.editCategories.setText(Language.get("edit_categories"))

        for shelf in SHELVES:
            shelf.configNewShelveLabel.setText(Language.get("shelf_question_1"))
            shelf.sidesNewShelf.setText(Language.get("shelf_question_2"))
            shelf.sidesNewShelfInput.trueButton.setText(Language.get("yes"))
            shelf.sidesNewShelfInput.falseButton.setText(Language.get("no"))
            shelf.configFloorsShelfLabel.setText(Language.get("shelf_question_4"))

        for store in STORES:
            store.goBackStore.setText(Language.get("go_back"))
            store.changeFloorButton.clear()

            for index in range(store.floor):
                store.changeFloorButton.addItem(Language.get("floor") + str(index + 1))

            for shelf in store.shelves:
                shelf.shelfNumber.setText(Language.get("shelf") + str(shelf.actualNumber) + ":")

                for space in shelf.spaces:
                    space.openSpaceConfig.setText(Language.get("go_back"))
                    space.labelCategory.setText(Language.get("category"))

                    space.category.showSpace.setText(Language.get("go_back"))
                    space.category.categoryNameLabel.setText(Language.get("category_name"))
                    space.category.categoryColorLabel.setText(Language.get("category_color"))
                    space.category.saveCategory.setText(Language.get("save"))
                    space.category.categoryColor.setText(Language.get("select_color"))
                    space.category.addCategory.setText(Language.get("add_category"))
                    space.category.newCategoryColorButton.setText(Language.get("select_color"))
                    space.category.cancelButtonAddCategory.setText(Language.get("cancel"))
                    space.category.createCategoryButton.setText(Language.get("create"))

                    space.category.addCategoryName.setPlaceholderText(Language.get("name"))
                    space.category.newCategoryProductLabel.setText(Language.get("category_has_product"))
                    space.category.newCategoryWithProduct.trueButton.setText(Language.get("yes"))
                    space.category.newCategoryWithProduct.falseButton.setText(Language.get("no"))

                    space.product.productLabel.setText(Language.get("product"))
                    space.product.addProduct.setText(Language.get("add_product"))
                    space.product.cancelAddProduct.setText(Language.get("cancel"))
                    space.product.productSelector.clear()
                    space.product.productSelector.addItem(Language.get("no_product"))

                    for prod in PRODUCTS_INFO:
                        space.product.productSelector.addItem(prod.name)
        
        self.WINDOW.reOpenHome()
        self.WINDOW.categorySpace.STORE.hideStore()
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x, y):
        self.changer.move(x, y)