from app_tests.utils.encrypt import Encrypt

def test_hash():
    string = "TEST"

    hashedString = Encrypt.hash(string)
    secondHashedString = Encrypt.hash(string)

    assert string == "TEST"
    assert hashedString != "TEST"
    assert secondHashedString != hashedString

def test_check():
    string = "TEST"
    wrongString = "tEST"

    hashedString = Encrypt.hash(string)
    secondHashedString = Encrypt.hash(string)

    assert Encrypt.check(hashedString, string) == True
    assert Encrypt.check(secondHashedString, string) == True

    assert Encrypt.check(hashedString, wrongString) == False
    assert Encrypt.check(secondHashedString, wrongString) == False