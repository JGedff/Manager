import json

class JsonManager():
    def getJson(path):
        with open(path, 'r', encoding="utf-8") as file:
            return json.load(file)

    def getLanguage(lang = "English"):
        match lang:
            case "English":
                with open("lang/en.json", 'r', encoding="utf-8") as file:
                    return json.load(file)
            case "Spanish":
                with open("lang/es.json", 'r', encoding="utf-8") as file:
                    return json.load(file)
            case "Catalan":
                with open("lang/ca.json", 'r', encoding="utf-8") as file:
                    return json.load(file)