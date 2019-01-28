import json

class PostCounterparty:
    def __init__(self, name, category, superCategory, logoUrl, homePageUrl, region):
        self.name = name
        self.category= category
        self.superCategory = superCategory
        self.logoUrl = logoUrl
        self.homePageUrl = homePageUrl
        self.region = region

    @staticmethod
    def load(path):
        with open(path, encoding="utf-8") as file:
            file_content = file.read()
        json_object = json.loads(file_content)
        return json_object

    def __str__(self):
        return self.name+"\t"+self.region
