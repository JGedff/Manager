def useLessFunction():
    pass

def getMaxFloor(arrayShelves):
    maxFloor = 1

    for shelf in arrayShelves:
        if maxFloor < shelf.floors:
            maxFloor = shelf.floors
    
    return maxFloor