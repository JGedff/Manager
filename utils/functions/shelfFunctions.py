from constants import SHELVES_FORMS, WINDOW_HEIGHT, WINDOW_WIDTH

from utils.language import Language

def saveShelfInfo():
    for shelf in SHELVES_FORMS:
        shelf.saveInfo()

def updateShelfPosition():
    x = 400
    y = 300

    for index, shelf in enumerate(SHELVES_FORMS):
        # Updates the position of the shelf
        shelf.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Updates the name of the shelf
        shelf.shelfLabel.setText(Language.get("shelf") + str(index + 1))

        y += 200