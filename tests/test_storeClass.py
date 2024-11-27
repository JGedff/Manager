from PyQt5.QtCore import Qt

from app_tests.constants import STORES, SHELVES, SHELVES_FORMS

from app_tests.utils.category import Category

from app_tests.main import Store, Shelf

#### TESTS ####

def test_store(qtbot):
    Category.addCategory("CATEGORY1", "white")
    Category.addCategory("CATEGORY2", "black")

    Shelf.createShelf(None)

    SHELVES_FORMS[0].spaces = 1
    SHELVES_FORMS[0].floors = 2

    store = Store("NEW STORE", None, 0, 0, None)

    STORES.append(store)

    store.hideStore()
    store.showIcon()

    assert store.storeIcon.isVisible()
    assert not store.changeFloorButton.isVisible()
    assert not store.goBackStore.isVisible()

    qtbot.mouseClick(store.storeIcon, Qt.LeftButton)

    assert not store.storeIcon.isVisible()
    assert store.changeFloorButton.isVisible()
    assert not store.goBackStore.isVisible()

    assert SHELVES[0][0].spaces[0].box.isVisible()
    assert not SHELVES[0][0].spaces[1].box.isVisible()

    store.changeFloorButton.setCurrentIndex(1)

    assert not SHELVES[0][0].spaces[0].box.isVisible()
    assert SHELVES[0][0].spaces[1].box.isVisible()

    qtbot.mouseClick(SHELVES[0][0].spaces[0].box, Qt.LeftButton)

    Store.configSpace(0) # This simulates what would happen when a space from the store was pressed

    assert not store.storeIcon.isVisible()
    assert not store.changeFloorButton.isVisible()
    assert store.goBackStore.isVisible()

    qtbot.mouseClick(store.goBackStore, Qt.LeftButton)

    assert not store.storeIcon.isVisible()
    assert store.changeFloorButton.isVisible()
    assert not store.goBackStore.isVisible()

    Category.delAll()
