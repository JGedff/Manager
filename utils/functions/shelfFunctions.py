from constants import SHELVES, WINDOW_HEIGHT, WINDOW_WIDTH

from utils.language import Language

def updateShelfPosition():
    x = 400
    y = 100

    for index, shelf in enumerate(SHELVES):
        # Updates the position of the shelf
        shelf.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Updates the name of the shelf
        shelf.configNewStoreLabel.setText(Language.get("shelf") + str(index + 1))

        y += 150