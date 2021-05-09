from pyowm import OWM
from pytz import UTC
from datetime import datetime, timedelta
from statistics import mean

import os

class WeatherService():

    def __init__(self):

        self.mgr = OWM(os.environ.get("OWM_KEY")).weather_manager() 
        self.long = os.environ.get("LONG")
        self.lat = os.environ.get("LAT")
        self.interval = "3h"
    
    def chance_of_rain(self) -> float:

        oneCall = self.mgr.one_call(self.lat, self.long)
        hourlyForecasts = oneCall.forecast_hourly
        nowPlusSix = UTC.localize(datetime.now() + timedelta(hours=6))

        fcst = [fcst.precipitation_probability \
            for fcst in hourlyForecasts \
            if fcst.reference_time("date") < nowPlusSix]

        pctChanceRain = max(fcst)

        return pctChanceRain
    
if __name__ == "__main__":

    ws = WeatherService()
    
    print("chance of rain:", ws.chance_of_rain())

