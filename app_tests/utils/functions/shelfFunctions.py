from app_tests.constants import WINDOW_HEIGHT, WINDOW_WIDTH

from app_tests.utils.language import Language

def saveShelfInfo(arrayShelfs):
    for shelf in arrayShelfs:
        shelf.saveInfo()

def updateShelfPosition(arrayShelfs):
    x = 400
    y = 300

    for index, shelf in enumerate(arrayShelfs):
        # Updates the position of the shelf
        shelf.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Updates the name of the shelf
        shelf.shelfLabel.setText(Language.get("shelf") + str(index + 1))

        y += 200
