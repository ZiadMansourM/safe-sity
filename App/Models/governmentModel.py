from Models.cityModel import CityModel
import string

class GovernmentModel():

    cities: dict = {}

    def __init__(self, inputCities):
        for city in inputCities:
            self.cities[city] = CityModel(inputCities[city])

    def getLicensePlates(self, city: string, street: string):
        if city not in list(self.cities.keys()):
            return None
        else:
            return self.cities[city].getLicensePlates(street)
