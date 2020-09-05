from CameraHelper import CameraHelper
from datetime import datetime
from json import dumps, load

import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "TelemetryConfiguration.json")

class TelemetryHelper(object):

    def __init__(
        self, 
        pressure = None, # float
        humidity = None, # float
        temperature = None, # float
        temperatureFromHumidity = None, # float 
        temperatureFromPressure = None, # float
        waterContent = None, # float
        pctChanceRain = None, # float
        lowWaterContent = None, # bool
        willNotRain = None, # bool
        fertilize = None, # bool
        decisionCode = None, # int
        decisionName = None, # string
        picturePath = None # string
    ): 
        self.camera = CameraHelper()
        self.pressure = pressure or float("inf")
        self.humidity = humidity or float("inf")
        self.temperature = temperature or float("inf")
        self.temperatureFromHumidity = temperatureFromHumidity or float("inf")
        self.temperatureFromPressure = temperatureFromPressure or float("inf")
        self.waterContent = waterContent or float("inf")
        self.pctChanceRain = pctChanceRain or float("inf")
        self.lowWaterContent = lowWaterContent or False
        self.willNotRain = willNotRain or False
        self.fertilize = fertilize or False
        self.decisionCode = decisionCode or -1
        self.decisionName = decisionName or "N/A"
        self.picturePath = picturePath or "N/A"

        jsonObj = self.__get_configuration()
        
        self.logPath = self.__get_log_location(jsonObj)

    def __enter__(self):

        return self
    
    def __exit__(self, exc_type, exc_value, traceback):

        self.pressure = None
        self.humidity = None
        self.temperature = None
        self.temperatureFromHumidity = None
        self.temperatureFromPressure = None
        self.waterContent = None
        self.pctChanceRain = None
        self.lowWaterContent = None
        self.willNotRain = None
        self.fertilize = None
        self.decisionCode = None
        self.picturePath = None
        self.logPath = None

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

    def take_picture(self):
        
        picturePath = self.camera.take_default_picture()
        
        self.picturePath = picturePath

        return picturePath
    
    def write_document(self):

        document = str(self)

        path = self.logPath
        path = path + "/groot-log-" + self.get_date_string() + ".json"

        f = open(path, "a")
        f.write(document)
        f.close()

        return path
    
    def collect_telemetry(self):

        picturePath = self.take_picture()
        print("picture available at: {}".format(picturePath))

        docPath = self.write_document()
        print("document available at: {}".format(docPath))

if __name__ == "__main__":

    with TelemetryHelper() as th:
        th.collect_telemetry()
