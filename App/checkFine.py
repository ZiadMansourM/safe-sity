from Models.fineDetailsModel import FineDetailsModel
import string

class CheckFine():
    fineDetails: FineDetailsModel = None
    def __init__(self, jsonFile: string):
        self.fineDetails = FineDetailsModel(jsonFile)
        pass

    def checkFine(self, licensePlate: string, government: string, city: string, street: string):
        if self.fineDetails.getLicensePlates(government, city, street) == None:
            return None
        else:
            return licensePlate