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
        self.WINDOW.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__()))
        self.WINDOW.createStoreButton.setText(Language.get("create_store"))
        self.WINDOW.editCategories.setText(Language.get("edit_categories"))
        self.WINDOW.storeNameLabel.setText(Language.get("name_store"))
        self.WINDOW.addStoreButton.setText(Language.get("add_store"))
        self.WINDOW.addShelfButton.setText(Language.get("add_shelf"))
        self.WINDOW.setWindowTitle(Language.get("window_title"))
        self.WINDOW.goHome.setText(Language.get("go_back"))

        self.WINDOW.configCategory.category.showSpace.setText(Language.get("go_back"))
        self.WINDOW.configCategory.category.saveCategory.setText(Language.get("save"))
        self.WINDOW.configCategory.category.addCategory.setText(Language.get("add_category"))
        self.WINDOW.configCategory.category.categoryColor.setText(Language.get("select_color"))
        self.WINDOW.configCategory.category.createCategoryButton.setText(Language.get("create"))
        self.WINDOW.configCategory.category.cancelButtonAddCategory.setText(Language.get("cancel"))
        self.WINDOW.configCategory.category.categoryNameLabel.setText(Language.get("category_name"))
        self.WINDOW.configCategory.category.addCategoryName.setPlaceholderText(Language.get("name"))
        self.WINDOW.configCategory.category.categoryColorLabel.setText(Language.get("category_color"))
        self.WINDOW.configCategory.category.newCategoryColorButton.setText(Language.get("select_color"))
        self.WINDOW.configCategory.category.newCategoryWithProduct.trueButton.setText(Language.get("yes"))
        self.WINDOW.configCategory.category.newCategoryWithProduct.falseButton.setText(Language.get("no"))
        self.WINDOW.configCategory.category.newCategoryProductLabel.setText(Language.get("category_has_product"))
        
        self.WINDOW.configCategory.product.productSelector.addItem(Language.get("no_product"))
        self.WINDOW.configCategory.product.cancelAddProduct.setText(Language.get("cancel"))
        self.WINDOW.configCategory.product.addProduct.setText(Language.get("add_product"))
        self.WINDOW.configCategory.product.productLabel.setText(Language.get("product"))
        self.WINDOW.configCategory.product.productSelector.clear()

        for prod in PRODUCTS_INFO:
            self.WINDOW.configCategory.product.productSelector.addItem(prod.name)

        # Shelf forms
        for shelfIndex, shelf in enumerate(SHELVES):
            shelf.inputSpacesLabel.setText(Language.get("shelf_question_1"))
            shelf.doubleShelfLabel.setText(Language.get("shelf_question_2"))
            shelf.doubleShelfInput.trueButton.setText(Language.get("yes"))
            shelf.doubleShelfInput.falseButton.setText(Language.get("no"))
            shelf.shelfFloorsLabel.setText(Language.get("shelf_question_4"))
            shelf.shelfLabel.setText(Language.get("shelf") + str(shelfIndex + 1))

        # Stores
        for store in STORES:
            store.goBackStore.setText(Language.get("go_back"))
            store.changeFloorButton.clear()

            for index in range(store.floor):
                store.changeFloorButton.addItem(Language.get("floor") + str(index + 1))

            # Shelf
            for shelf in store.shelves:
                shelf.shelfNumber.setText(Language.get("shelf") + str(shelf.actualNumber) + ":")

                # Space
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
        self.WINDOW.configCategory.STORE.hideStore()
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x, y):
        self.changer.move(x, y)