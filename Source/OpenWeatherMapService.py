from pyowm import OWM
from pytz import UTC
from datetime import datetime, timedelta
from statistics import mean
from json import load
from TelemetryHelper import TelemetryHelper

import os.path

CONFIGURATION_PATH = os.path.join("Configuration","OpenWeatherMapServiceConfiguration.json")

class OpenWeatherMapService():

    def __init__(self,telemetryHelper: TelemetryHelper = None, token: str = None):
            
        token = token or self.__getToken()

        if not token:
            raise TypeError("Token can not be null or empty. \
                Get token from: https://openweathermap.org/api")
        
        self._mgr = OWM(token).weather_manager() 
        self._telemetry = telemetryHelper or TelemetryHelper()
        self._pRainThreshold = 0.7
        self._long = -77.14379 # longitude of ipc
        self._lat = 38.94417 # latitude of ipc
        self._interval = "3h"

    def __getToken(self)-> str:
        with open (CONFIGURATION_PATH) as f:
            j = load(f)
            token = j["token"]
            return token
    
    def will_rain(self, threshold: float = None) -> bool:

        tRain = threshold or self._pRainThreshold

        # call "one call" api from open weather map to get intraday 
        # forecast at lat/long of church.
        oneCall = self._mgr.one_call(self._lat, self._long)

        # get property of one call response that holds forecasts
        hourlyForecasts = oneCall.forecast_hourly

        # log max forecast
        self._telemetry.pctChanceRain = max([fcst.precipitation_probability for fcst in hourlyForecasts])

        print("[2]: percentage chance of rain is " + str(self._telemetry.pctChanceRain))

        # add six hours to the current time so we can use this value to
        # filter out forecasts for weather that occurs more than 6 hours
        # from the current time.
        nowPlusSix = UTC.localize(datetime.now() + timedelta(hours=6))

        # select/extract the probability of rain (precipitation_probability)
        # for each forecast (fcst) in hourly forecasts (hourlyForecasts)
        # if the time of the forecast is less than six hours from now 
        # and the probability of precipitation is greater than or equal
        # to the rain thershold. 
        fcst = [{"probability": fcst.precipitation_probability, \
            "time": fcst.reference_time("date").strftime("%m/%d/%Y, %H:%M:%S")} \
            for fcst in hourlyForecasts \
            if fcst.reference_time("date") < nowPlusSix \
                and fcst.precipitation_probability >= tRain]

        # if there are any forecasts left over after filtering we will assume
        # it will rain in the next six hours.
        willRain = fcst is not None and fcst is not []

        return willRain

    def will_rain_english(self) -> str:

        willItRain = self.will_rain()
        word = "yes" if willItRain else "no"

        return word

    def will_rain_numeric(self) -> int:

        willItRain = self.will_rain()
        num = 1 if willItRain else 0

        return num 
    
if __name__ == "__main__":

    owma = OpenWeatherMapService()
    willItRainToday = owma.will_rain_english()

    print("Is it going to rain today at IPC?", willItRainToday)
