from datetime import datetime
from json import load, dumps
from MegaioHelper import MegaioHelper
from WateringDecisionMaker import WateringDecisionMaker
from TelemetryHelper import TelemetryHelper
from time import sleep

import uuid
import os.path

ACTION_NONE = 0
ACTION_RAIN = 1
ACTION_WATER = 2
ACTION_WATER_AND_FERTILIZE = 3
CONFIGURATION_PATH = os.path.join("Configuration", "SystemConfiguration.json")

class Groot(object):

    def __init__(self, cycles = None):
        
        jsonObj = self.__get_configuration()

        self.cycles = cycles or self.__get_cycles(jsonObj) 
        self.cycleDays = self.__get_cycle_days()
        self.cycleHours = self.__get_cycle_hours()
        self.telemetryHelper = TelemetryHelper()
        self.decisionMaker = WateringDecisionMaker(self.telemetryHelper) 
        self.megaioHelper = MegaioHelper()

    def __str__(self):

        return dumps(str(self.__dict__))

    def __get_configuration(self):

        jsonFile = open(CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_cycles(self, jsonObj):

        cycles = jsonObj["cycles"]

        return cycles 
    
    def __get_cycle_days(self):

        cycleDays = [cycle["day"] for cycle in self.cycles]

        return cycleDays
    
    def __get_cycle_hours(self):

        cycleHours = set()

        for cycle in self.cycles:

            cycleStart = cycle["start"]
            cycleEnd = cycle["end"]

            hourRange = self.get_hour_range(cycleStart, cycleEnd)

            for hour in hourRange:
                cycleHours.add(hour)
        
        return cycleHours
    
    def get_hour_range(self, startHour, endHour):

        if startHour < 0 or startHour > 23:
            raise Exception("Invalid input for cycle_start_time in SystemConfiguration.json. The cycle_start_time argument must be greater than or equal to one and less than or equal to 24.")

        if endHour < 0 or endHour > 23:
            raise Exception("Invalid input for cycle_end_time in SystemConfiguration.json. The cycle_end_time argument must be greater than or equal to one and less than or equal to 24.")

        L = []
        S = startHour
        E = endHour

        while S != E:
            L.append(S)
            S += 1
            if S > 23:
                S = 0
        
        return L

    def check_and_water(self):

        decision = self.decisionMaker.water()
        decisionString = self.decision_to_human_readable(decision)
        
        self.telemetryHelper.algoDecision = decisionString

        if decision == ACTION_WATER:
            self.megaioHelper.pump_water()
        
        if decision == ACTION_WATER_AND_FERTILIZE:
            self.megaioHelper.fertilize_and_water()
    
    def decision_to_human_readable(self, code):

        d = {
            ACTION_NONE : "NO ACTION",
            ACTION_RAIN : "IT IS GOING TO RAIN",
            ACTION_WATER : "WATERING GARDEN",
            ACTION_WATER_AND_FERTILIZE : "WATERING AND FERTILIZING GARDEN"
        }

        if(code in list(d.keys())):
            return d[code]
        else:
            return "INVALID DECISION CODE"
    
    def run_schedule(self):

        now = datetime.now()
        nameOfCurrentDay = now.strftime("%A").upper()
        currentHour = now.hour
        print("Current Hour: {}".format(str(currentHour)))
        if nameOfCurrentDay in self.cycleDays:
            if currentHour in self.cycleHours:
                self.check_and_water()

    def SYS_START(self):

        sessionId = str(uuid.uuid4())

        while(True):
            runid = str(uuid.uuid4())
            telDocument = {
                "sessionid": sessionId,
                "runid": runid,
                "createDate": self.telemetryHelper.get_date_string()}

            try:
                self.run_schedule()
                self.telemetryHelper.write_telemetry_cloud(telDocument)

            except Exception as e:
                exDoc = { "exception": str(e) }
                telDocument.update(exDoc)
                
                try:
                    self.telemetryHelper.write_telemetry_cloud(telDocument)
                
                except Exception as ex:
                    innerExDoc = { "innerException": str(ex) }
                    telDocument.update(innerExDoc)
                    self.telemetryHelper.write_telemetry_local(telDocument)

# Test

if __name__ == "__main__":

    groot = Groot()

    groot.SYS_START()


        



    


