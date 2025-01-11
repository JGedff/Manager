import pytest

from app.constants import CATEGORY_COLORS, CATEGORY_NAMES

from app.utils.category import Category

def test_changeCategoryColor():
    assert CATEGORY_COLORS[0] == "#976431"

    Category.changeCategoryColor(0, "#EEEAAA")

    assert CATEGORY_COLORS[0] == "#EEEAAA"

def test_changeCategoryName():
    assert CATEGORY_NAMES[0] == "Unreachable"

    Category.changeCategoryName(0, "CHANGE_NAME")

    assert CATEGORY_NAMES[0] == "CHANGE_NAME"

def test_addCategory():
    with pytest.raises(IndexError) as exc_info:
        CATEGORY_NAMES[2]
    assert str(exc_info.value) == "list index out of range"

    with pytest.raises(IndexError) as exc_info2:
        CATEGORY_COLORS[2]
    assert str(exc_info2.value) == "list index out of range"

    Category.addCategory("NEWONE", "#455664")

    assert CATEGORY_NAMES[2] == "NEWONE"
    assert CATEGORY_COLORS[2] == "#455664"

def test_delCategory():
    assert CATEGORY_NAMES[2] == "NEWONE"
    assert CATEGORY_COLORS[2] == "#455664"

    Category.delCategory(2)

    with pytest.raises(IndexError) as exc_info:
        CATEGORY_NAMES[2]
    assert str(exc_info.value) == "list index out of range"

    with pytest.raises(IndexError) as exc_info2:
        CATEGORY_COLORS[2]
    assert str(exc_info2.value) == "list index out of range"

def test_getIndexByName():
    assert Category.getIndexByName("Unexistent") == -1
    assert Category.getIndexByName("CHANGE_NAME") == 0

def test_getColorByName():
    assert Category.getColorByName("Unexistent") == "#000000"
    assert Category.getColorByName("CHANGE_NAME") == "#EEEAAA"

def test_getNameByIndex():
    assert Category.getNameByIndex(0) == "CHANGE_NAME"

    with pytest.raises(IndexError) as exc_info:
        Category.getNameByIndex(5)
    assert str(exc_info.value) == "list index out of range"
