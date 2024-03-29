from json import load, dumps
from MegaioHelper import MegaioHelper
from TelemetryHelper import TelemetryHelper
from datetime import datetime
from OpenWeatherMapService import OpenWeatherMapService

import os.path

ACTION_NONE = 0
ACTION_RAIN = 1
ACTION_WATER = 2
ACTION_WATER_AND_FERTILIZE = 3
CONFIGURATION_PATH = os.path.join("Configuration","WateringDecisionMakerConfiguration.json")

class WateringDecisionMaker(object):
    
    def __init__(self, telemetryHelper: TelemetryHelper = None):

        jsonObj = self.__get_config()
        self.targetPctRain = self.__get_target_percent_chance_rain(jsonObj) 
        self.targetWcth = self.__get_target_water_content_high(jsonObj)
        self.targetWctl = self.__get_target_water_content_low(jsonObj)
        self.fertilizerDays = self.__get_fertilizer_days(jsonObj)
        self.megaioHelper = MegaioHelper()
        self.telemetryHelper = telemetryHelper or TelemetryHelper()
        self.openWeatherMapService = OpenWeatherMapService(self.telemetryHelper)
    
    def __str__(self):

        return dumps(str(self.__dict__))

    def __get_config(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj
    
    def __get_target_percent_chance_rain(self, jsonObj):

        target = jsonObj["target_percent_chance_rain"]

        return target

    def __get_target_water_content_high(self, jsonObj):

        target = jsonObj["target_water_content_high"]

        return target

    def __get_target_water_content_low(self, jsonObj):

        target = jsonObj["target_water_content_low"]

        return target

    def __get_fertilizer_days(self, jsonObj):

        days = jsonObj["fertilizer_days"]

        return days
        
    def check_rain(self):

        shouldWater = not self.openWeatherMapService.will_rain(self.targetPctRain)
        
        return shouldWater
        
    def check_water_content(self):

        waterContent = self.megaioHelper.get_water_content()
        self.telemetryHelper.soilWaterContent = waterContent
        
        print("[1]: percentage normalized water content is " + str(waterContent))

        shouldWater = True if waterContent < self.targetWctl else False

        return shouldWater

    def check_fertilizer(self):

        currentDate = datetime.now()
        nameOfDay = currentDate.strftime("%A").upper()

        print("[3]: current day is " + nameOfDay + ", fertilizer days are " + str(self.fertilizerDays))

        shouldFertilize = True if nameOfDay in self.fertilizerDays else False 

        return shouldFertilize

    def water(self):

        lowWaterContent = self.check_water_content()
        wontRain = self.check_rain()
        fertilize = self.check_fertilizer()
        
        print("- Garden soil has low water content? " + str(lowWaterContent))
        print("- Will not rain? " + str(wontRain))
        print("- Scheduled to fertilize today? " + str(fertilize))

        if lowWaterContent:     
            if wontRain:
                if fertilize: 
                    return ACTION_WATER_AND_FERTILIZE
                return ACTION_WATER
            return ACTION_RAIN
        return ACTION_NONE

# Tests

if __name__ == "__main__":

    telHelper = TelemetryHelper()
    wdm = WateringDecisionMaker(telHelper)
    # waterContent = wdm.check_water_content()
    # shouldFertilize = wdm.check_fertilizer()
    rain = wdm.check_rain()

    #waterCode = wdm.water()

    # print(str(wdm))
    # print("water content: " + str(waterContent))
    # print("should fertilize: " + str(shouldFertilize))
    print("should water : " + str(rain))
    # print("water Code: " + str(waterCode))
