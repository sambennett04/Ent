from sense_hat import SenseHat
from json import dumps, load

import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "SenseHatConfiguration.json")

class SenseHatHelper(object):

    def __init__(self):

        self.senseHat = SenseHat()

        jsonObj = self.__get_configuration()
        
        self.senseHat.rotation = self.__get_rotation(jsonObj)
        self.textColorR = self.__get_text_color_r(jsonObj)
        self.textColorG = self.__get_text_color_g(jsonObj)
        self.textColorB = self.__get_text_color_b(jsonObj)

        self.lastReading = self.get_reading()

    def __str__(self):

        return dumps(str(self.__dict__))
    
    def __get_configuration(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_rotation(self, jsonObj):

        rotation = jsonObj["rotation"]

        return rotation

    def __get_text_color_r(self, jsonObj):

        r = jsonObj["color"]["r"]

        return r

    def __get_text_color_g(self, jsonObj):

        g = jsonObj["color"]["g"]

        return g

    def __get_text_color_b(self, jsonObj):
        
        b = jsonObj["color"]["b"]

        return b

    def show_message(self, message):

        self.senseHat.show_message(message, text_colour=[self.textColorR, self.textColorG, self.textColorB])

    def get_reading(self):

        reading = {}

        reading["pressure"] = self.senseHat.get_pressure()
        reading["humidity"] = self.senseHat.get_humidity()
        reading["temperature"] = self.senseHat.get_temperature()
        reading["temperature_from_humidity"] = self.senseHat.get_temperature_from_humidity()
        reading["temperature_from_pressure"] = self.senseHat.get_temperature_from_pressure()

        self.lastReading = reading
        
        return reading
    
    def show_reading(self):

        reading = self.lastReading

        for key in reading.keys():

            message = key + " : " + str(reading[key])
            self.show_message(message)

if __name__ == "__main__":

    sh = SenseHatHelper()
    sh.show_message("I am Groot!")

    sh.show_reading()
