import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

from app.styles.colorFunctions import getStyleSheet
from app.utils.category import Category

from app.main import ShelfInfo

#### TESTS ####

def test_checkInfoShelfCorrect():
    info_doubleShelf_11Spaces_2Floors = ShelfInfo(0, 0, 2, 11, True, 2)

    assert info_doubleShelf_11Spaces_2Floors.shelfNumber.text() == "Shelf 1:"

    assert info_doubleShelf_11Spaces_2Floors.spacesLength == 11
    assert info_doubleShelf_11Spaces_2Floors.spaces.__len__() == 22

    for index, space in enumerate(info_doubleShelf_11Spaces_2Floors.spaces):
        if index != 10 and index != 21:
            assert not space.long
        else:
            assert space.long
