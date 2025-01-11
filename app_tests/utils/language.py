from app_tests.utils.json import JsonManager

class Language():
    lang = "English"
    info = JsonManager.getLanguage("English")

    @classmethod
    def changeTo(cls, language):
        cls.lang = language
        cls.info = JsonManager.getLanguage(language)

        if language != "Español" and language != "Català":
            cls.lang = "English"
    
    @classmethod
    def get(cls, string):
        return cls.info[string]