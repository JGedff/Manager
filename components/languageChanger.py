from PyQt5.QtWidgets import QLabel, QComboBox

from utils.language import Language

from constants import WINDOW_HEIGHT, STORES, SHELVES_FORMS, SHELVES

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

        self.WINDOW.categoryManager.showSpace.setText(Language.get("go_back"))
        self.WINDOW.categoryManager.saveCategory.setText(Language.get("save"))
        self.WINDOW.categoryManager.addCategory.setText(Language.get("add_category"))
        self.WINDOW.categoryManager.categoryColor.setText(Language.get("select_color"))
        self.WINDOW.categoryManager.createCategoryButton.setText(Language.get("create"))
        self.WINDOW.categoryManager.cancelButtonAddCategory.setText(Language.get("cancel"))
        self.WINDOW.categoryManager.categoryNameLabel.setText(Language.get("category_name"))
        self.WINDOW.categoryManager.addCategoryName.setPlaceholderText(Language.get("name"))
        self.WINDOW.categoryManager.categoryColorLabel.setText(Language.get("category_color"))
        self.WINDOW.categoryManager.newCategoryColorButton.setText(Language.get("select_color"))
        
        # Shelf forms
        for shelfIndex, shelf in enumerate(SHELVES_FORMS):
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
        for storage in SHELVES:
            for shelf in storage:
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
        
        self.WINDOW.reOpenHome()
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x, y):
        self.changer.move(x, y)