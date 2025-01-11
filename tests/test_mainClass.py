import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from tests.functions.constantsForTest import WINDOWS

from app.utils.mongoDb import Mongo

from app.constants import DEFAULT_IMAGE, SHELVES_FORMS, STORES

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def main_window(qtbot):
    window = WINDOWS.mainWindow
    qtbot.addWidget(window)
    return window

#### TESTS ####

def test_addShelfForm(qtbot, main_window):
    main_window.show()

    assert SHELVES_FORMS.__len__() == 2

    qtbot.mouseClick(main_window.addStoreButton, Qt.LeftButton)
    qtbot.mouseClick(main_window.addShelfButton, Qt.LeftButton)
    
    assert SHELVES_FORMS.__len__() == 3
    assert SHELVES_FORMS[2].isVisible()

    qtbot.mouseClick(SHELVES_FORMS[2].delShelfButton, Qt.LeftButton)

def test_addStoreForm(qtbot, main_window):
    Mongo.closeMongoConnection()

    assert STORES.__len__() == 0
    assert SHELVES_FORMS.__len__() == 2
    
    qtbot.mouseClick(main_window.createStoreButton, Qt.LeftButton)

    assert STORES.__len__() == 1
    assert SHELVES_FORMS.__len__() == 0

    WINDOWS.resetGlobalVariables()

def test_showHideObjectsMain(qtbot, monkeypatch, main_window):
    main_window.show()

    assert main_window.addStoreButton.isVisible()
    assert main_window.editCategories.isVisible()
    assert main_window.languageChanger.changer.isVisible()

    assert not main_window.goHome.isVisible()
    assert not main_window.formStoreIcon.isVisible()
    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.storeNameInput.isVisible()
    assert not main_window.storeNameLabel.isVisible()
    assert not main_window.addShelfButton.isVisible()
    assert not main_window.createStoreButton.isVisible()
    assert not main_window.footerFormBackground.isVisible()
    assert not main_window.headerFormBackground.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()

    qtbot.mouseClick(main_window.editCategories, Qt.LeftButton)

    assert main_window.goHome.isVisible()
    assert main_window.categoryManager.addCategory.isVisible()

    assert not main_window.formStoreIcon.isVisible()
    assert not main_window.editCategories.isVisible()
    assert not main_window.addStoreButton.isVisible()
    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.storeNameInput.isVisible()
    assert not main_window.storeNameLabel.isVisible()
    assert not main_window.addShelfButton.isVisible()
    assert not main_window.createStoreButton.isVisible()
    assert not main_window.footerFormBackground.isVisible()
    assert not main_window.headerFormBackground.isVisible()
    assert not main_window.languageChanger.changer.isVisible()

    qtbot.mouseClick(main_window.goHome, Qt.LeftButton)

    assert main_window.addStoreButton.isVisible()
    assert main_window.editCategories.isVisible()
    assert main_window.languageChanger.changer.isVisible()

    assert not main_window.goHome.isVisible()
    assert not main_window.formStoreIcon.isVisible()
    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.storeNameInput.isVisible()
    assert not main_window.storeNameLabel.isVisible()
    assert not main_window.addShelfButton.isVisible()
    assert not main_window.createStoreButton.isVisible()
    assert not main_window.footerFormBackground.isVisible()
    assert not main_window.headerFormBackground.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()

    qtbot.mouseClick(main_window.addStoreButton, Qt.LeftButton)

    assert main_window.goHome.isVisible()
    assert main_window.formStoreIcon.isVisible()
    assert main_window.storeNameInput.isVisible()
    assert main_window.storeNameLabel.isVisible()
    assert main_window.addShelfButton.isVisible()
    assert main_window.createStoreButton.isVisible()
    assert main_window.footerFormBackground.isVisible()
    assert main_window.headerFormBackground.isVisible()

    assert not main_window.addStoreButton.isVisible()
    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.editCategories.isVisible()
    assert not main_window.languageChanger.changer.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()

    # Define the mock function
    def mock_getOpenFileName(parent=None, caption="", directory="", filter=""):
        return "image.png", "Image Files (*.png *.jpg *.jpeg *.bmp)"

    # Replace QFileDialog.getOpenFileName with the mock
    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)

    assert main_window.image == DEFAULT_IMAGE

    qtbot.mouseClick(main_window.formStoreIcon, Qt.LeftButton) # MOCK INPUT FILE

    assert main_window.goHome.isVisible()
    assert main_window.image != DEFAULT_IMAGE
    assert main_window.formStoreIcon.isVisible()
    assert main_window.storeNameInput.isVisible()
    assert main_window.storeNameLabel.isVisible()
    assert main_window.addShelfButton.isVisible()
    assert main_window.createStoreButton.isVisible()
    assert main_window.footerFormBackground.isVisible()
    assert main_window.headerFormBackground.isVisible()
    assert main_window.setDefaultIcon.isVisible()

    assert not main_window.addStoreButton.isVisible()
    assert not main_window.editCategories.isVisible()
    assert not main_window.languageChanger.changer.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()

    qtbot.mouseClick(main_window.setDefaultIcon, Qt.LeftButton)

    assert main_window.goHome.isVisible()
    assert main_window.formStoreIcon.isVisible()
    assert main_window.storeNameInput.isVisible()
    assert main_window.storeNameLabel.isVisible()
    assert main_window.addShelfButton.isVisible()
    assert main_window.createStoreButton.isVisible()
    assert main_window.footerFormBackground.isVisible()
    assert main_window.headerFormBackground.isVisible()

    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.addStoreButton.isVisible()
    assert not main_window.editCategories.isVisible()
    assert not main_window.languageChanger.changer.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()

    qtbot.mouseClick(main_window.goHome, Qt.LeftButton)

    assert main_window.addStoreButton.isVisible()
    assert main_window.editCategories.isVisible()
    assert main_window.languageChanger.changer.isVisible()

    assert not main_window.goHome.isVisible()
    assert not main_window.formStoreIcon.isVisible()
    assert not main_window.setDefaultIcon.isVisible()
    assert not main_window.storeNameInput.isVisible()
    assert not main_window.storeNameLabel.isVisible()
    assert not main_window.addShelfButton.isVisible()
    assert not main_window.createStoreButton.isVisible()
    assert not main_window.footerFormBackground.isVisible()
    assert not main_window.headerFormBackground.isVisible()
    assert not main_window.categoryManager.addCategory.isVisible()
