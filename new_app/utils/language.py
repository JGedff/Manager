from utils.json import JsonManager

class Language():
    _lang = "English"
    _info = JsonManager.get_language("English")

    @classmethod
    def change_language(cls, language):
        cls._lang = language
        cls._info = JsonManager.get_language(language)

        if language != "Español" and language != "Català":
            cls._lang = "English"
    
    @classmethod
    def get(cls, string):
        return cls._info[string]
