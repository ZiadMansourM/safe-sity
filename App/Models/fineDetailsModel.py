from Models.governmentModel import GovernmentModel
import string, json

class FineDetailsModel():

    governements: dict = {}
    jsonData: dict = {}

    def __init__(self, jsonFile):
        self.loadJsonFile(jsonFile)
        for governement in self.jsonData:
            self.governements[governement] = GovernmentModel(self.jsonData[governement])


    def loadJsonFile(self, jsonFile: string):
        file = open (jsonFile, "r")
        self.jsonData = json.loads(file.read())

    def getLicensePlates(self, government: string, city: string, street: string):
        if government not in list(self.governements.keys()):
            return None
        else:
            return self.governements[government].getLicensePlates(city, street)
    
        