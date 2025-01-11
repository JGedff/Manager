import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog

from app_tests.utils.functions.spaceCategoryFunctions import createCategoryIn, updateNameCategory, deleteCategoryFrom
from app_tests.styles.colorFunctions import getStyleSheet
from app_tests.utils.category import Category
from app_tests.main import SpaceCategory

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def space_category(qtbot):
    categoryEditor = SpaceCategory()
    qtbot.addWidget(categoryEditor)
    return categoryEditor

#### TESTS ####

def test_showHideUI(space_category):
    Category.addCategory("NEW CATEGORY", "#0F0F0F")
    createCategoryIn(space_category, "NEW CATEGORY", None)

    assert space_category.doubleButtons.__len__() == 1

    for button in space_category.doubleButtons:
        assert not button.isVisible()

    space_category.showUI()

    for button in space_category.doubleButtons:
        assert button.isVisible()
    
    assert space_category.addCategory.isVisible()

    space_category.hideUI()

    for button in space_category.doubleButtons:
        assert not button.isVisible()
    
    assert not space_category.addCategory.isVisible()

    space_category.showUI()

def test_showHideOptionsToAddCategory(qtbot, space_category):
    assert not space_category.addCategoryName.isVisible()
    assert not space_category.createCategoryButton.isVisible()
    assert not space_category.newCategoryColorButton.isVisible()
    assert not space_category.cancelButtonAddCategory.isVisible()
    
    for button in space_category.doubleButtons:
        assert button.button2.isEnabled()

    qtbot.mouseClick(space_category.addCategory, Qt.LeftButton)

    assert space_category.addCategoryName.isVisible()
    assert space_category.createCategoryButton.isVisible()
    assert space_category.newCategoryColorButton.isVisible()
    assert space_category.cancelButtonAddCategory.isVisible()

    for button in space_category.doubleButtons:
        assert not button.button2.isEnabled()
    
    assert not space_category.addCategory.isEnabled()

    qtbot.mouseClick(space_category.cancelButtonAddCategory, Qt.LeftButton)

    assert not space_category.addCategoryName.isVisible()
    assert not space_category.createCategoryButton.isVisible()
    assert not space_category.newCategoryColorButton.isVisible()
    assert not space_category.cancelButtonAddCategory.isVisible()

    for button in space_category.doubleButtons:
        assert button.button2.isEnabled()
    
    assert space_category.addCategory.isEnabled()

def test_createCategory(qtbot, monkeypatch, space_category):
    qtbot.mouseClick(space_category.addCategory, Qt.LeftButton)

    def mock_getColor():
        return QColor("red")  # Simulate user selecting "red" in the QColorDialog

    monkeypatch.setattr(QColorDialog, "getColor", mock_getColor)

    assert space_category.newCategoryName == ""
    assert space_category.newCategoryColor == ""
    assert not space_category.createCategoryButton.isEnabled()

    qtbot.mouseClick(space_category.addCategoryName, Qt.LeftButton)
    qtbot.keyClicks(space_category.addCategoryName, "CATEGORY")

    qtbot.mouseClick(space_category.newCategoryColorButton, Qt.LeftButton)

    assert space_category.newCategoryName == "CATEGORY"
    assert space_category.newCategoryColor == QColor("red").name()
    assert space_category.createCategoryButton.isEnabled()

    qtbot.mouseClick(space_category.createCategoryButton, Qt.LeftButton)

    assert not space_category.addCategoryName.isVisible()
    assert not space_category.createCategoryButton.isVisible()
    assert not space_category.newCategoryColorButton.isVisible()
    assert not space_category.cancelButtonAddCategory.isVisible()

    for button in space_category.doubleButtons:
        assert button.button2.isEnabled()

def test_openCategoryConfigAndGoBack(qtbot, space_category):
    space_category.showUI()

    assert space_category.addCategory.isVisible()

    for button in space_category.doubleButtons:
        assert button.button2.isVisible()

    qtbot.mouseClick(space_category.doubleButtons[0].button1, Qt.LeftButton)

    assert not space_category.addCategory.isVisible()

    for button in space_category.doubleButtons:
        assert not button.button2.isVisible()
    
    assert space_category.showSpace.isVisible()
    assert space_category.categoryNameLabel.isVisible()
    assert space_category.categoryColorLabel.isVisible()
    assert space_category.saveCategory.isVisible()
    assert space_category.categoryColor.isVisible()
    assert space_category.categoryName.isVisible()

    assert space_category.categoryColor.styleSheet() == getStyleSheet(Category.getColorByName(space_category.nameModifiedCategory))

    space_category.shortcut = True # There isn't any shelf in this moment, so if the shortcut is false, it will crash, because it tries to access to the shelfs.

    qtbot.mouseClick(space_category.showSpace, Qt.LeftButton)

    assert space_category.addCategory.isVisible()

    for button in space_category.doubleButtons:
        assert button.button2.isVisible()
    
    assert not space_category.showSpace.isVisible()
    assert not space_category.categoryNameLabel.isVisible()
    assert not space_category.categoryColorLabel.isVisible()
    assert not space_category.saveCategory.isVisible()
    assert not space_category.categoryColor.isVisible()
    assert not space_category.categoryName.isVisible()

def test_editCategory(qtbot, monkeypatch, space_category):
    space_category.shortcut = True

    oldCategoryName = space_category.doubleButtons[0].textButton1()

    qtbot.mouseClick(space_category.doubleButtons[0].button1, Qt.LeftButton)

    def mock_getColor():
        return QColor("black")  # Simulate user selecting "red" in the QColorDialog

    monkeypatch.setattr(QColorDialog, "getColor", mock_getColor)

    qtbot.mouseClick(space_category.categoryName, Qt.LeftButton)
    qtbot.keyClicks(space_category.categoryName, "MODIFY CATEGORY")

    qtbot.mouseClick(space_category.categoryColor, Qt.LeftButton)

    assert space_category.nameModifiedCategory != space_category.categoryName.text()
    assert space_category.colorModifiedCategory != space_category.newColor

    qtbot.mouseClick(space_category.saveCategory, Qt.LeftButton)
    qtbot.mouseClick(space_category.showSpace, Qt.LeftButton)

    # This function is here because the function that saves and updates the information, uses global variables to update all spaces, but like this space is not linked to any shelf or store, they have to be runned manually
    updateNameCategory(space_category, space_category.colorModifiedCategory, oldCategoryName, space_category.nameModifiedCategory, True)

    assert space_category.doubleButtons[0].textButton1() == "Modify category"
    assert Category.getColorByName("Modify category") == QColor("black").name()

def test_deleteCategory(qtbot, space_category):
    oldNameCategory1 = space_category.doubleButtons[0].textButton1()

    assert Category.getNameByIndex(0) == oldNameCategory1

    qtbot.mouseClick(space_category.doubleButtons[0].button2, Qt.LeftButton)

    # This function is here because the function that saves and updates the information, uses global variables to update all spaces, but like this space is not linked to any shelf or store, they have to be runned manually
    deleteCategoryFrom(space_category, 0, oldNameCategory1, True)

    assert Category.getNameByIndex(0) != oldNameCategory1
    assert space_category.doubleButtons[0].textButton1() != oldNameCategory1

    Category.delAll()