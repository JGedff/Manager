def useless_function():
    pass

def get_max_floor(shelves):
    max_floor = 1

    for form in shelves:
        if max_floor < form.get_num_floors():
            max_floor = form.get_num_floors()
    
    return max_floor