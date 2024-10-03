def checkIsNum(numToCheck):
    try:
        int(numToCheck)
        return True
    except ValueError:
        return False