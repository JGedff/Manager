def useLessFunction():
    pass

def updateNameCategory(space, color, actualName, newName, index):
    if space.category.color == color:
        # Change the name of the button with the actual category to the new name for the category
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)
                break

        # Updates the name in the comboBox
        space.configCategory.setItemText(0, newName)

        # Updates the name in the space
        space.category.name = newName
    else:
        # Change the name of the button with the actual category to the new name for the category
        for button in space.category.doubleButtons:
            if button.textButton1() == actualName:
                button.setTextButton1(newName)
                break
        
        # Updates the name in the comboBox
        space.configCategory.setItemText(index, newName)