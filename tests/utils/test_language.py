from test_json import ENJSON, ESJSON, CAJSON

from app_tests.utils.language import Language

def test_changeTo():
    assert Language.lang == "English"
    assert Language.info == ENJSON

    Language.changeTo("Català")

    assert Language.lang == "Català"
    assert Language.info == CAJSON

    Language.changeTo("Español")

    assert Language.lang == "Español"
    assert Language.info == ESJSON

    Language.changeTo("UNEXISTENT")

    assert Language.lang == "English"
    assert Language.info == ENJSON

def test_get():
    assert Language.get("window_title") == "Manager"

    Language.changeTo("Català")
    
    assert Language.get("window_title") == "Gestor"
    
    Language.changeTo("Español")

    assert Language.get("window_title") == "Gestor"
    
    Language.changeTo("English")

    assert Language.get("window_title") == "Manager"