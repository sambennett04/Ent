from json import load, dumps
from time import sleep
from statistics import mean
from SenseHatHelper import SenseHatHelper
from megaio import set_relay, get_adc

import os.path

RELAY_ON = 1
RELAY_OFF = 0
MEGAIO_CONFIGURATION_PATH = os.path.join("Configuration","MegaioConfiguration.json")
SENSOR_CONFIGURATION_PATH = os.path.join("Configuration", "WaterSensorConfiguration.json")

class MegaioHelper(object):

    def __init__(self, wateringRelayGroup = None, fertilizingRelayGroup = None, wateringWaitTime = None, fertilizingWaitTime = None, signalUpperBound = None, signalLowerBound = None, sensorStack = None, sensorChannel = None):

        self.sense = SenseHatHelper()

        jsonObj = self.__get_megaio_config()

        self.wRelayGroup = wateringRelayGroup or self.__get_watering_relay_group(jsonObj)
        self.fRelayGroup = fertilizingRelayGroup or self.__get_fertilizing_relay_group(jsonObj)
        self.wWaitTime = wateringWaitTime or self.__get_watering_wait_time(jsonObj)
        self.fWaitTime = fertilizingWaitTime or self.__get_fertilizing_wait_time(jsonObj)

        jsonObj = self.__get_sensor_config()

        self.slBound = signalLowerBound or self.__get_signal_lower_bound(jsonObj)
        self.suBound = signalUpperBound or self.__get_signal_upper_bound(jsonObj)
        self.stack = sensorStack or self.__get_sensor_stack(jsonObj)
        self.channel = sensorChannel or self.__get_sensor_channel(jsonObj)

    def __str__(self):

        return dumps(str(self.__dict__))

    def __get_megaio_config(self):

        jsonFile = open(MEGAIO_CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_sensor_config(self):

        jsonFile = open(SENSOR_CONFIGURATION_PATH, "r")
        jsonObj = load(jsonFile)
        jsonFile.close()

        return jsonObj

    def __get_signal_lower_bound(self, jsonObj):

        signalLowerBound = jsonObj["signal_lower_bound"]

        return signalLowerBound

    def __get_signal_upper_bound(self, jsonObj):

        signalUpperBound = jsonObj["signal_upper_bound"]

        return signalUpperBound

    def __get_watering_relay_group(self, jsonObj):

        wateringRelayGroup = jsonObj["watering_relay_group"]

        return wateringRelayGroup

    def __get_fertilizing_relay_group(self, jsonObj):

        fertilizingRelayGroup = jsonObj["fertilizing_relay_group"]

        return fertilizingRelayGroup

    def __get_watering_wait_time(self, jsonObj):

        wateringWaitTime = jsonObj["watering_wait_time"]

        return wateringWaitTime

    def __get_fertilizing_wait_time(self, jsonObj):

        fertilizingWaitTime = jsonObj["fertilizing_wait_time"]

        return fertilizingWaitTime

    def __get_sensor_stack(self, jsonObj):

        sensorStack = jsonObj["sensor_stack"]

        return sensorStack

    def __get_sensor_channel(self, jsonObj):

        sensorChannel = jsonObj["sensor_channel"]

        return sensorChannel

    def relay_on(self, stack, relay):

        set_relay(stack, relay, RELAY_ON)

    def relay_off(self, stack, relay):

        set_relay(stack, relay, RELAY_OFF)

    def on_wait_off(self, relayInfo, time):

        # check and handle pump state

        for info in relayInfo:
            stack = info["stack"]
            relay = info["relay"]
            self.relay_on(stack, relay)

        sleep(time)

        for info in relayInfo:
            stack = info["stack"]
            relay = info["relay"]
            self.relay_off(stack, relay)

    def pump_water(self):

        self.on_wait_off(self.wRelayGroup, self.wWaitTime)

    def pump_fertilizer(self):

        self.on_wait_off(self.fRelayGroup, self.fWaitTime)

    def fertilize_and_water(self):

        self.pump_fertilizer()
        self.pump_water()

    def fertilize_and_water_interleaved(self):

        minWait = min(self.wWaitTime, self.fWaitTime)
        maxWait = max(self.wWaitTime, self.fWaitTime)
        difWait = maxWait - minWait

        self.relay_on(self.wRelayGroup[0]["stack"], self.wRelayGroup[0]["relay"])
        self.relay_on(self.fRelayGroup[0]["stack"], self.fRelayGroup[0]["relay"])
        print("[INFO]: Water and fertilizer running...")

        sleep(minWait)

        if self.wWaitTime == minWait:
            print("Water shut off in first cycle after wait time of: " + str(self.wWaitTime))
            self.relay_off(self.wRelayGroup[0]["stack"], self.wRelayGroup[0]["relay"])

        if self.fWaitTime == minWait:
            print("Fertilizer shut off in first cycle after wait time of: " + str(self.fWaitTime))
            self.relay_off(self.fRelayGroup[0]["stack"], self.fRelayGroup[0]["relay"])

        sleep(difWait)

        totalWait = minWait + difWait

        if self.wWaitTime == totalWait:
            print("Water shuf off in second cycle after wait time of: " + str(totalWait))
            self.relay_off(self.wRelayGroup[0]["stack"], self.wRelayGroup[0]["relay"])

        if self.fWaitTime == totalWait:
            print("Fertilizer shut off in second cycle after wait time of: " + str(totalWait))
            self.relay_off(self.fRelayGroup[0]["stack"], self.fRelayGroup[0]["relay"])

    def get_water_content(self):

        sample = [get_adc(self.stack, self.channel) for i in range(100)]
        sampleMean = mean(sample)

        if sampleMean >= self.suBound:
            return 0

        if sampleMean <= self.slBound:
            return 1

        print("sample mean: " + str(sampleMean))
        onePctPts = ((self.suBound - self.slBound) / 100.0)
        print("one percent points: " + str(onePctPts))
        normalizedReadingPts = sampleMean - self.slBound
        print("normalized reading: " + str(normalizedReadingPts))
        pctWaterContent = normalizedReadingPts / onePctPts
        pctWaterContent = (100 - pctWaterContent) / 100
        print("decimal water content: " + str(pctWaterContent))

        return pctWaterContent

# Tests

if __name__ == "__main__":

    mh = MegaioHelper()
    # shutdown to clear system in case of conflicting/bad runs
    mh.relay_off(mh.fRelayGroup[0]["stack"], mh.fRelayGroup[0]["relay"])
    mh.relay_off(mh.wRelayGroup[0]["stack"], mh.wRelayGroup[0]["relay"])

    print(str(mh))

    # mh.pump_fertilizer()
    # mh.pump_water()
    # mh.fertilize_and_water()
    mh.fertilize_and_water_interleaved()
    # mh.pump_fertilizer()

    wc = mh.get_water_content()
    print("the percentage of water in the soil is: " + str(wc * 100.0) + " %")
