from app.utils.functions.globalFunctions import useLessFunction, getMaxFloor

class Floor():
    def __init__(self, floors):
        self.floors = floors

def test_useless():
    assert useLessFunction() == None

def test_getMaxFloor():
    assert getMaxFloor([Floor(5), Floor(2), Floor(1), Floor(10)]) == 10