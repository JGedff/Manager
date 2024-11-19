import pytest

from app.main import SpaceCategory, Space

from app.utils.category import Category
from app.utils.functions.spaceCategoryFunctions import createCategoryIn, updateNameCategory, deleteCategoryFrom, updateButtonsPosition, setEmptyCategory, setUnreachableCategory, setCategoryByName, getEmptyCategoryName, getUnreachableCategoryName

#### CREATE NEEDED OBJECTS ####

@pytest.fixture
def spaceCategoryMain(qtbot):
    space_category = SpaceCategory()
    qtbot.addWidget(space_category)
    return space_category

@pytest.fixture
def space1(qtbot):
    space = Space(0, 0, 1, 1, 1, 1, 1, 1)
    qtbot.addWidget(space)
    return space

#### TESTS ####

def test_createCategoryIn(spaceCategoryMain, space1):
    with pytest.raises(IndexError) as exc_info:
        spaceCategoryMain.doubleButtons[0]
    assert str(exc_info.value) == "list index out of range"

    with pytest.raises(IndexError) as exc_info2:
        space1.category.doubleButtons[0]
    assert str(exc_info2.value) == "list index out of range"

    createCategoryIn(spaceCategoryMain, "TEST", None, True)
    createCategoryIn(space1, "TEST", None)

    assert spaceCategoryMain.doubleButtons[0].textButton1() == "TEST"
    assert space1.category.doubleButtons[0].textButton1() == "TEST"

def test_updateNameCategory(spaceCategoryMain, space1):
    createCategoryIn(spaceCategoryMain, "TEST", None, True)
    createCategoryIn(space1, "TEST", None)

    updateNameCategory(spaceCategoryMain, "#FFFFFF", "TEST", "YES", True)
    updateNameCategory(space1, "#FFFFFF", "TEST", "YES")

    assert spaceCategoryMain.doubleButtons[0].textButton1() == "YES"
    assert space1.category.doubleButtons[0].textButton1() == "YES"

def test_deleteCategoryFrom(spaceCategoryMain, space1):
    createCategoryIn(spaceCategoryMain, "TEST", None, True)
    createCategoryIn(space1, "TEST", None)

    with pytest.raises(IndexError) as exc_info1:
        deleteCategoryFrom(spaceCategoryMain, 1, "TEST", True)
    assert str(exc_info1.value) == "list index out of range"

    with pytest.raises(IndexError) as exc_info2:
        deleteCategoryFrom(space1, 1, "TEST")
    assert str(exc_info2.value) == "list index out of range"

    deleteCategoryFrom(spaceCategoryMain, 0, "TEST", True)
    deleteCategoryFrom(space1, 0, "TEST")

    with pytest.raises(IndexError) as exc_info3:
        spaceCategoryMain.doubleButtons[0]
    assert str(exc_info3.value) == "list index out of range"

    with pytest.raises(IndexError) as exc_info4:
        space1.category.doubleButtons[0]
    assert str(exc_info4.value) == "list index out of range"

def test_updateButtonsPosition(spaceCategoryMain, space1):
    Category.addCategory("TEST", "#FFFFFF")
    Category.addCategory("SECOND", "#EA3DFB")

    createCategoryIn(spaceCategoryMain, "TEST", None, True)
    createCategoryIn(space1, "TEST", None)

    createCategoryIn(spaceCategoryMain, "SECOND", None, True)
    createCategoryIn(space1, "SECOND", None)

    assert spaceCategoryMain.doubleButtons[0].geometry().x() == 0
    assert spaceCategoryMain.doubleButtons[0].geometry().y() == 0
    assert spaceCategoryMain.doubleButtons[1].geometry().x() == 0
    assert spaceCategoryMain.doubleButtons[1].geometry().y() == 0

    assert space1.category.doubleButtons[0].geometry().x() == 0
    assert space1.category.doubleButtons[0].geometry().y() == 0
    assert space1.category.doubleButtons[1].geometry().x() == 0
    assert space1.category.doubleButtons[1].geometry().y() == 0

    updateButtonsPosition(spaceCategoryMain, True)
    updateButtonsPosition(space1)

    assert spaceCategoryMain.doubleButtons[0].geometry().x() != 0
    assert spaceCategoryMain.doubleButtons[0].geometry().y() != 0
    assert spaceCategoryMain.doubleButtons[1].geometry().x() != 0
    assert spaceCategoryMain.doubleButtons[1].geometry().y() != 0

    assert space1.category.doubleButtons[0].geometry().x() != 0
    assert space1.category.doubleButtons[0].geometry().y() != 0
    assert space1.category.doubleButtons[1].geometry().x() != 0
    assert space1.category.doubleButtons[1].geometry().y() != 0

def test_setEmptyCategory(space1):
    Category.delCategory(0)
    Category.delCategory(0)
    
    Category.addCategory("Empty", "#123456")

    assert space1.category.name == "TEST"
    assert space1.category.color == "#FFFFFF"

    setEmptyCategory(space1.category)

    assert space1.category.name == "Empty"
    assert space1.category.color == "#123456"

def test_setUnreachableCategory(space1):
    Category.addCategory("Unreachable", "#976431")

    assert space1.category.name == "Empty"
    assert space1.category.color == "#123456"

    setUnreachableCategory(space1.category)

    assert space1.category.name == "Unreachable"
    assert space1.category.color == "#976431"

def test_setCategoryByName(space1):
    assert space1.category.name == "Empty"
    assert space1.category.color == "#123456"

    setCategoryByName(space1.category, "Unreachable")

    assert space1.category.name == "Unreachable"
    assert space1.category.color == "#976431"

def test_getEmptyCategoryName():
    assert getEmptyCategoryName() == "Empty"

    Category.delCategory(0)
    
    assert getEmptyCategoryName() == "Unreachable"

    Category.addCategory("Unreachable", "#976431")

def test_getUnreachableCategoryName():
    assert getUnreachableCategoryName() == "Unreachable"

    Category.delCategory(0)
    Category.addCategory("NEW", "#AAAAAA")

    assert getUnreachableCategoryName() == "NEW"