from utils.json import JsonManager

class Language():
    lang = "English"
    info = JsonManager.get_language("English")

    @classmethod
    def change_language(cls, language):
        cls.lang = language
        cls.info = JsonManager.get_language(language)

        if language != "Español" and language != "Català":
            cls.lang = "English"
    
    @classmethod
    def get(cls, string):
        return cls.info[string]