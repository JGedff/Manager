from PyQt5.QtWidgets import QLabel, QComboBox

from app_tests.styles.styleSheets import COMBO_BOX
from app_tests.styles.fonts import FONT_SMALL_TEXT

from app_tests.constants import WINDOW_HEIGHT, STORES, SHELVES_FORMS, SHELVES

from app_tests.utils.language import Language

class LanguageChanger(QLabel):
    def __init__(self, window, parent, mainWindow = False):
        super().__init__(parent)

        self.initVariables(window, mainWindow)
        self.initUI(parent)
        self.initEvents()

    def initVariables(self, window, mainWindow):
        self.language = 'English'
        self.WINDOW = window
        self.mainWindow = mainWindow

    def initUI(self,parent):
        self.changer = QComboBox(parent)
        self.changer.addItem("English")
        self.changer.addItem("Español")
        self.changer.addItem("Català")

        self.changer.setFont(FONT_SMALL_TEXT)
        self.changer.setGeometry(15, WINDOW_HEIGHT - 50, 100, 25)
        self.changer.setStyleSheet(COMBO_BOX)
    
    def initEvents(self):
        self.changer.currentTextChanged.connect(self.changeLang)

    def changeLang(self, language):
        Language.changeTo(language)

        self.updateUI()
        self.language = language

    def updateUI(self):
        if self.mainWindow:
            self.WINDOW.storeNameInput.setPlaceholderText(Language.get("store") + str(STORES.__len__() + 1))
            self.WINDOW.createStoreButton.setText(Language.get("create_store"))
            self.WINDOW.editCategories.setText(Language.get("edit_categories"))
            self.WINDOW.setDefaultIcon.setText(Language.get("default_image"))
            self.WINDOW.formStoreIcon.setText(Language.get("change_image"))
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
                shelf.doubleShelfInput.setTrueText(Language.get("yes"))
                shelf.doubleShelfInput.setFalseText(Language.get("no"))
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
        else:
            self.WINDOW.setWindowTitle(Language.get("log_in"))
            self.WINDOW.logInTitle.setText(Language.get("log_in"))
            self.WINDOW.userLabel.setText(Language.get("user_name"))
            self.WINDOW.passwordLabel.setText(Language.get("password"))
            self.WINDOW.registerTitle.setText(Language.get("register"))
            self.WINDOW.accessOfflineButton.setText(Language.get("access_offline"))
            self.WINDOW.repeatPasswordLabel.setText(Language.get("repeat_password"))
            self.WINDOW.userQLineEdit.setPlaceholderText(Language.get("enter_user_name"))
            self.WINDOW.passwordQLineEdit.setPlaceholderText(Language.get("enter_password"))
            self.WINDOW.repeatPasswordQLineEdit.setPlaceholderText(Language.get("enter_password"))

            if self.WINDOW.logIn:
                self.WINDOW.logInButton.setText(Language.get("log_in"))
                self.WINDOW.registerButton.setText(Language.get("register"))
            else:
                self.WINDOW.logInButton.setText(Language.get("register"))
                self.WINDOW.registerButton.setText(Language.get("log_in"))
    
    def hide(self):
        self.changer.hide()

    def show(self):
        self.changer.show()

    def raise_(self):
        self.changer.raise_()

    def move(self, x, y):
        self.changer.move(x, y)

    def setGeometry(self, x, y, width, height):
        self.changer.setGeometry(x, y, width, height)

    def setCurrentText(self, item):
        self.changer.setCurrentText(item)