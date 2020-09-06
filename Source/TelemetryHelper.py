from CosmosHelper import CosmosHelper
from datetime import datetime
from json import dumps, load

import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "TelemetryConfiguration.json")

class TelemetryHelper(object):

    def __init__(
        self, 
        pressure: float = None,
        humidity: float = None,
        temperature: float = None,
        temperatureFromHumidity: float = None,
        temperatureFromPressure: float = None,
        soilWaterContent: float = None,
        pctChanceRain: float = None,
        algoDecision: str = None
    ): 
        self.pressure = pressure or float("inf")
        self.humidity = humidity or float("inf")
        self.temperature = temperature or float("inf")
        self.temperatureFromHumidity = temperatureFromHumidity or float("inf")
        self.temperatureFromPressure = temperatureFromPressure or float("inf")
        self.soilWaterContent = soilWaterContent or float("inf")
        self.pctChanceRain = pctChanceRain or float("inf")
        self.algoDecision = algoDecision or str()

        jsonObj = self.__get_configuration()
        
        self.logPath = self.__get_log_location(jsonObj)
        self.__cosmosHelper = CosmosHelper()

    def __str__(self):

        return dumps(str(self.__dict__))
    
    def __get_configuration(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_log_location(self, jsonObj):

        logLocation = jsonObj["log_storage"]

        return logLocation
    
    def get_date_string(self):

        now = datetime.now()
        dateString = now.strftime("%Y-%m-%d-%H:%M:%S")

        return dateString
    
    def generate_telemetry_dict(self):

        telemetryDict = {
            "pressure": self.pressure,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "temperatureFromHumidity": self.temperatureFromHumidity,
            "temperatureFromPressure": self.temperatureFromPressure,
            "soilWaterContent": self.soilWaterContent,
            "pctChanceRain": self.pctChanceRain,
            "algoDecision": self.algoDecision
        }

        return telemetryDict
    
    def write_telemetry_local(self, document: str = None):

        document = document or str(self.generate_telemetry_dict())

        path = self.logPath
        path = path + "/groot-log-" + self.get_date_string() + ".json"

        f = open(path, "w")
        f.write(document)
        f.close()

        return path
    
    def write_telemetry_cloud(self, document: dict = None):
        
        document = document or {}
        document.update(self.generate_telemetry_dict())
        result = self.__cosmosHelper.write_document(document)
        
        return result

if __name__ == "__main__":

    helper = TelemetryHelper(
        pressure = 1.0,
        humidity = 1.0,
        temperature = 65,
        temperatureFromHumidity = 65.0, 
        temperatureFromPressure = 65.0,
        soilWaterContent = 0.5,
        pctChanceRain = 0.5,
        algoDecision = "IT IS GOING TO RAIN"
    )

    print(str(helper))

    document = {"sessionid": "unittest"}

    helper.write_telemetry_cloud(document)