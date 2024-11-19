from constants import SHELVES_FORMS

def useLessFunction():
    pass

def getMaxFloor():
    maxFloor = 1

    for shelf in SHELVES_FORMS:
        if maxFloor < shelf.floors:
            maxFloor = shelf.floors
    
    return maxFloor