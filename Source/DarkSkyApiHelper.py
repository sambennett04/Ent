from darksky.api import DarkSky
from darksky.types import languages, units, weather
from json import load, dumps
from statistics import mean
from datetime import datetime

import os.path

CONFIGURATION_PATH = os.path.join("Configuration", "DarkSkyConfiguration.json")

class DarkSkyApiHelper(object):

    def __init__(self, latitude = None, longitude = None, sampleRange = None):

        jsonObj = self.__get_config()
        apiKey = self.__get_api_secret(jsonObj)

        self.longitude = longitude or self.__get_longitude(jsonObj)
        self.latitude = latitude or self.__get_latitude(jsonObj)
        self.sampleRange = sampleRange or self.__get_sample_forecast_range(jsonObj)
        self.client = DarkSky(apiKey)
    
    def __str__(self):

        return dumps(str(self.__dict__))
    
    def __get_config(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_api_secret(self, jsonObj):

        apiKey = jsonObj["api_key"]

        return apiKey
    
    def __get_latitude(self, jsonObj):

        lat = jsonObj["latitude"]

        return lat

    def __get_longitude(self, jsonObj):

        lon = jsonObj["longitude"]

        return lon
    
    def __get_sample_forecast_range(self, jsonObj):

        sampleRange = jsonObj["sample_forecast_range_hours"]

        return sampleRange

    def get_weather_forecast(self):

        forecast = self.client.get_forecast(
            self.latitude, 
            self.longitude
        )

        return forecast

    def get_pct_chance_of_rain(self):

        forecast = self.get_weather_forecast()
        
        now = datetime.now()
        hour = now.hour
        date = now.date()

        hourlyData = forecast.hourly.data
        hourlyPctRain = [x.precip_probability for x in hourlyData if (hour + self.sampleRange) > x.time.hour >= hour and x.time.date() == date]
        pRain = mean(hourlyPctRain)

        return pRain

# Tests
if __name__ == "__main__":

    helper = DarkSkyApiHelper()
    print(str(helper))
    print(str(helper.get_weather_forecast()))
    print(str(helper.get_pct_chance_of_rain()))