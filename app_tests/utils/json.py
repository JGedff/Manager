import json

class JsonManager():
    @staticmethod
    def getJson(path):
        with open(path, 'r', encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def getLanguage(lang = "English"):
        match lang:
            case "English":
                return JsonManager.getJson('lang/en.json')
            case "Español":
                return JsonManager.getJson('lang/es.json')
            case "Català":
                return JsonManager.getJson('lang/ca.json')

        return JsonManager.getJson('lang/en.json')