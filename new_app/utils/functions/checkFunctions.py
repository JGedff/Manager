def is_num(numToCheck):
    try:
        int(numToCheck)
        return True
    except ValueError:
        return False

def is_decimal(numToCheck):
    try:
        float(numToCheck)
        return True
    except ValueError:
        return False