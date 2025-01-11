import pytest

from app.main import Shelf

from app.utils.functions.globalFunctions import useLessFunction, getMaxFloor

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def shelf1(qtbot):
    shelf_object = Shelf("", 0, 0)
    qtbot.addWidget(shelf_object)
    return shelf_object

@pytest.fixture
def shelf2(qtbot):
    shelf_object = Shelf("", 0, 0)
    qtbot.addWidget(shelf_object)
    return shelf_object

@pytest.fixture
def shelf3(qtbot):
    shelf_object = Shelf("", 0, 0)
    qtbot.addWidget(shelf_object)
    return shelf_object

#### TESTS ####

def test_useless():
    assert useLessFunction() == None

def test_getMaxFloor(shelf1, shelf2, shelf3):
    shelf1.floors = 10
    shelf2.floors = 5
    shelf3.floors = 15

    assert getMaxFloor([shelf1, shelf2, shelf3]) == 15