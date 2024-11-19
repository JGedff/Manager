import pytest

from app.main import Shelf

from app.utils.functions.shelfFunctions import saveShelfInfo, updateShelfPosition

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def shelf4(qtbot):
    shelf_object = Shelf("", 0, 0)
    qtbot.addWidget(shelf_object)
    return shelf_object

@pytest.fixture
def shelf5(qtbot):
    shelf_object = Shelf("", 0, 0)
    qtbot.addWidget(shelf_object)
    return shelf_object

#### TESTS ####

def test_saveShelfInfo(shelf4):
    assert shelf4.spaces == 1
    assert shelf4.floors == 1
    assert shelf4.double_shelf == False

    shelf4.inputSpaces.setValue(5)
    shelf4.shelfFloorsInput.setValue(10)
    shelf4.doubleShelfInput.setValue(True)

    saveShelfInfo([shelf4])

    assert shelf4.spaces == 5
    assert shelf4.floors == 10
    assert shelf4.double_shelf == True

def test_updateShelfPosition(shelf4, shelf5):
    updateShelfPosition([shelf5, shelf4])

    assert shelf4.geometry().x() == 400
    assert shelf4.geometry().y() == 500

    assert shelf5.geometry().x() == 400
    assert shelf5.geometry().y() == 300