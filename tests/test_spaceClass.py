import pytest

from PyQt5.QtCore import Qt

from app.styles.colorFunctions import getStyleSheet
from app.utils.category import Category

from app.main import Space

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def long_space(qtbot):
    Category.addCategory("Empty", "#FFFFFF")
    Category.addCategory("Fill", "#5F2A66")

    space = Space(0, 0, 1, 1, 0, 0, 1, 0, None, True)
    space.updateSpaceColor()

    qtbot.addWidget(space)
    
    Category.delAll()
    return space

#### TESTS ####

def test_showFloor(long_space):

    long_space.showFloor(1)

    assert long_space.box.isVisible()

    long_space.showFloor(10)

    assert not long_space.box.isVisible()

    long_space.showFloor(1)

def test_openSpaceConfig(qtbot, long_space):
    long_space.showFloor(1)

    assert long_space.box.isVisible()
    assert not long_space.configBox.isVisible()
    assert not long_space.shelfNumber.isVisible()
    assert not long_space.labelCategory.isVisible()
    assert not long_space.editCategories.isVisible()
    assert not long_space.openSpaceConfig.isVisible()
    assert not long_space.categorySelector.isVisible()

    qtbot.mouseClick(long_space.box, Qt.LeftButton)

    assert not long_space.box.isVisible()
    assert long_space.configBox.isVisible()
    assert long_space.shelfNumber.isVisible()
    assert long_space.labelCategory.isVisible()
    assert long_space.editCategories.isVisible()
    assert long_space.categorySelector.isVisible()
    assert not long_space.openSpaceConfig.isVisible()

def test_openCloseEditCategories(qtbot, long_space):
    qtbot.mouseClick(long_space.box, Qt.LeftButton)

    assert not long_space.box.isVisible()
    assert long_space.configBox.isVisible()
    assert long_space.shelfNumber.isVisible()
    assert long_space.labelCategory.isVisible()
    assert long_space.editCategories.isVisible()
    assert long_space.categorySelector.isVisible()
    assert not long_space.openSpaceConfig.isVisible()

    qtbot.mouseClick(long_space.editCategories, Qt.LeftButton)

    assert not long_space.box.isVisible()
    assert not long_space.configBox.isVisible()
    assert not long_space.shelfNumber.isVisible()
    assert not long_space.labelCategory.isVisible()
    assert not long_space.editCategories.isVisible()
    assert not long_space.categorySelector.isVisible()
    assert long_space.openSpaceConfig.isVisible()

    qtbot.mouseClick(long_space.openSpaceConfig, Qt.LeftButton)

    assert not long_space.box.isVisible()
    assert long_space.configBox.isVisible()
    assert long_space.shelfNumber.isVisible()
    assert long_space.labelCategory.isVisible()
    assert long_space.editCategories.isVisible()
    assert long_space.categorySelector.isVisible()
    assert not long_space.openSpaceConfig.isVisible()

def test_changeSpaceCategory(qtbot, long_space):
    qtbot.mouseClick(long_space.box, Qt.LeftButton)

    assert not long_space.box.isVisible()
    assert long_space.configBox.isVisible()
    assert long_space.shelfNumber.isVisible()
    assert long_space.labelCategory.isVisible()
    assert long_space.editCategories.isVisible()
    assert long_space.categorySelector.isVisible()
    assert not long_space.openSpaceConfig.isVisible()

    assert long_space.box.styleSheet() == getStyleSheet("#FFFFFF")
    assert long_space.configBox.styleSheet() == getStyleSheet("#FFFFFF")

    # This simulates the logic executed after a user changes the item in the QComboBox categorySelector
    long_space.categorySelector.setCurrentText("Fill")
    long_space.category.name = "Fill"
    long_space.category.color = "#5F2A66"

    long_space.updateSpaceColor()

    assert long_space.box.styleSheet() == getStyleSheet("#5F2A66")
    assert long_space.configBox.styleSheet() == getStyleSheet("#5F2A66")
