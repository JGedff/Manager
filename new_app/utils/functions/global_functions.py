def useless_function():
    pass

def get_max_floor(shelves):
    max_floor = 1

    for shelf in shelves:
        if max_floor < shelf.floors:
            max_floor = shelf.floors
    
    return max_floor