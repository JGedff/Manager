import json

class JsonManager():
    @staticmethod
    def get_json(path):
        with open(path, 'r', encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def get_language(lang = "English"):
        match lang:
            case "English":
                return JsonManager.get_json('lang/en.json')
            case "Español":
                return JsonManager.get_json('lang/es.json')
            case "Català":
                return JsonManager.get_json('lang/ca.json')

        return JsonManager.get_json('lang/en.json')