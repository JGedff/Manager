from app_tests.utils.functions.checkFunctions import checkIsNum

def test_checkIsNum():
    assert checkIsNum("8") == True
    assert checkIsNum(8) == True
    assert checkIsNum(0.8) == True
    assert checkIsNum("A") == False