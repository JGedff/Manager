from constants import WINDOW_HEIGHT, WINDOW_WIDTH

from utils.language import Language

def save_shelves_info(shelves: list):
    for form in shelves:
        form.save_info()

def update_shelves_pos(shelves: list):
    x = 400
    y = 300

    for index, form in enumerate(shelves):
        # Updates the position of the shelf
        form.setGeometry(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Updates the name of the shelf
        form.shelf_label.setText(Language.get("shelf") + str(index + 1))

        y += 200
