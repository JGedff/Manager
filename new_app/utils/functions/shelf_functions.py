from constants import WINDOW_HEIGHT, WINDOW_WIDTH

from utils.language import Language

def save_shelves_info(shelves):
    for shelf in shelves:
        shelf.save_info()

def update_shelves_pos(shelves):
    x = 400
    y = 300

    for index, shelf in enumerate(shelves):
        # Updates the position of the shelf
        shelf.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Updates the name of the shelf
        shelf.shelf_label.setText(Language.get("shelf") + str(index + 1))

        y += 200
