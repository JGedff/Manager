def useLessFunction():
    pass

def updateNameCategory(space, color, actualName, newName, index):
    if space.category.color == color:
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)

        space.configCategory.setItemText(0, newName)
        space.category.name = newName
    else:
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)

        space.configCategory.setItemText(index, newName)