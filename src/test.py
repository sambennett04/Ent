from actuation_service import ActuationService
from data_service import DataService
from decision_service import DecisionService
from default_values import CLOUD_ENABLED, WEATHER_ENABLED, DECISION_ENABLED
from weather_service import WeatherService

import automationhat as ah
import os
import time
import unittest

class EntTest(unittest.TestCase):
	
	def setUp(self):
		
		if(CLOUD_ENABLED):
			self.dataService = DataService()
		
		if(WEATHER_ENABLED):
			self.weatherService = WeatherService()
		
		if(DECISION_ENABLED):
			self.weatherService = WeatherService()
	
	def tearDown(self):
		
		if(CLOUD_ENABLED):
			del self.dataService
		
		if(WEATHER_ENABLED):
			del self.weatherService
		
		if(DECISION_ENABLED):
			del self.decisionService
	
# region ActuationService

	def test_actuation_service_get_sensor(self):
		
		data = ActuationService.get_sensor()
		print("sensor reading:", str(data))
		
		self.assertGreater(data, 0.03)
		
	def test_actuation_service_valve_open(self):
		
		ActuationService.valve_open()
		isOpen = ah.relay.one.is_on()
		time.sleep(5)
		print("is valve one open (should be true):", str(isOpen))
		
		self.assertTrue(isOpen)
		
	def test_actuation_service_valve_close(self):
		
		ActuationService.valve_close()
		isOpen = ah.relay.one.is_on()
		print("is relay one open (should be false):", str(isOpen))
		
		self.assertFalse(isOpen)
	
	def test_actuation_service_pump_on(self):
		
		ActuationService.pump_on()
		isOn = ah.output.one.is_on()
		time.sleep(5)
		print("is output channel one on (should be true):", str(isOn))
		
		self.assertTrue(isOn)
	
	def test_actuation_service_pump_off(self):
		
		ActuationService.pump_off()
		isOn = ah.output.one.is_on()
		print("is output channel one on (should be false):", str(isOn))
		
		self.assertFalse(isOn)

# endregion

# region Dataservice
	
	def test_data_service_write_document(self):
		
		if(CLOUD_ENABLED):
		
			doc = { "id": "unit-test-key", "value": 0 }
			result = dataService.write_document(doc)
			self.assertTrue(result)
		
		else:
			
			self.assertTrue(True)

#endregion

# region WeatherService 
	
	def test_weather_service_chance_of_rain(self):
		
		if(WEATHER_ENABLED):
		
			chanceOfRain = self.weatherService.chance_of_rain()
			self.assertGreaterEqual(chanceOfRain, 0.0)
		
		else:
			
			self.assertTrue(True)
		
# endregion

#region DecisionService
	
	def test_decision_service_make_decision(self):
		
		if(WEATHER_ENABLED and DESCISION_ENABLED):
		
			waterContent = ActuationService.get_sensor()
			rainChance = self.weatherService.chance_of_rain()
			decision = self.decisionService.make_decision(waterContent, decision)
			self.assertContains([self.decisionService.DO_NOTHING, \
				self.decisionService.DO_WATER, \
				self.decisionService.DO_WATER_AND_FERTILIZER], 
				decision)
				
		else:
			
			self.assertTrue(True)

# endregion

if __name__ == "__main__":
	
	unittest.main()
