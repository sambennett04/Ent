from pyowm import OWM
from pytz import UTC
from datetime import datetime, timedelta
from default_values import LAT, LONG, OMW_KEY
from statistics import mean

import os

class WeatherService():

    def __init__(self):
        
        __key = os.environ.get("OWM_KEY") or OMW_KEY
        
        self.long = os.environ.get("LONG") or LONG
        self.lat = os.environ.get("LAT") or LAT
        self.interval = "3h"
        self.mgr = OWM(__key).weather_manager() 
    
    def chance_of_rain(self) -> float:

        oneCall = self.mgr.one_call(self.lat, self.long)
        hourlyForecasts = oneCall.forecast_hourly
        nowPlusSix = UTC.localize(datetime.now() + timedelta(hours=6))

        fcst = [fcst.precipitation_probability \
            for fcst in hourlyForecasts \
            if fcst.reference_time("date") < nowPlusSix]

        pctChanceRain = max(fcst)

        return pctChanceRain
