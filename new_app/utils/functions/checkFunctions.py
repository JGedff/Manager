def is_num(numToCheck):
    try:
        int(numToCheck)
        return True
    except ValueError:
        return False

def checkIsDecimal(numToCheck):
    try:
        float(numToCheck)
        return True
    except ValueError:
        return False