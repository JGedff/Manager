import pytest

from PyQt5.QtCore import Qt

from app_tests.constants import SHELVES_FORMS

from app_tests.main import Shelf

#### CREATE NEEDED OBJECTS ####

Shelf.createShelf(None)
Shelf.createShelf(None)

@pytest.fixture
def shelf_form1(qtbot):
    shelf = SHELVES_FORMS[0]
    qtbot.addWidget(shelf)
    return shelf

@pytest.fixture
def shelf_form2(qtbot):
    shelf = SHELVES_FORMS[1]
    qtbot.addWidget(shelf)
    return shelf

#### TESTS ####

def test_showHideForm(shelf_form1, shelf_form2):
    assert not shelf_form1.isVisible()
    assert not shelf_form2.isVisible()

    Shelf.showAllForms()

    assert shelf_form1.isVisible()
    assert shelf_form2.isVisible()

    Shelf.hideAllForms()

    assert not shelf_form1.isVisible()
    assert not shelf_form2.isVisible()

def test_delShelf(qtbot, shelf_form1, shelf_form2):
    assert SHELVES_FORMS.__len__() == 2

    Shelf.showAllForms()

    with pytest.raises(AttributeError) as exc_info:
        shelf_form1.delShelfButton == None
    assert str(exc_info.value) == "'Shelf' object has no attribute 'delShelfButton'"

    assert shelf_form2.delShelfButton != None

    qtbot.mouseClick(shelf_form2.delShelfButton, Qt.LeftButton)

    assert shelf_form1.isVisible()
    assert not shelf_form2.isVisible()

    assert SHELVES_FORMS.__len__() == 1

def test_saveInfoForms(shelf_form1):
    assert shelf_form1.spaces == 1
    assert shelf_form1.floors == 1
    assert shelf_form1.double_shelf == False

    shelf_form1.inputSpaces.setValue(10)
    shelf_form1.shelfFloorsInput.setValue(2)
    shelf_form1.doubleShelfInput.setValue(True)

    assert shelf_form1.spaces == 1
    assert shelf_form1.floors == 1
    assert shelf_form1.double_shelf == False

    shelf_form1.saveInfo()

    assert shelf_form1.spaces == 10
    assert shelf_form1.floors == 2
    assert shelf_form1.double_shelf == True