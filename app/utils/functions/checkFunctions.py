from decimal import Decimal

def checkIsNum(numToCheck):
    try:
        int(numToCheck)
        return True
    except ValueError:
        return False

def checkIsDecimal(numToCheck):
    try:
        Decimal(numToCheck)
        return True
    except ValueError:
        return False