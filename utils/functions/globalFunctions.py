from constants import SHELVES

def useLessFunction():
    pass

def getMaxFloor():
    maxFloor = 1

    for shelf in SHELVES:
        if maxFloor < shelf.floors:
            maxFloor = shelf.floors
    
    return maxFloor