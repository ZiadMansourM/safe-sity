from Models.streetModel import StreetModel
import string
class CityModel(): 

    streets: dict = {}

    def __init__(self, inputStreets:dict) -> None:
        for street in inputStreets:
            self.streets[street] = StreetModel(inputStreets[street])

    def getLicensePlates(self, street: string):
        if street not in list(self.streets.keys()):
            return None
        else:
            return street
