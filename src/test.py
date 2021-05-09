from actuation_service import ActuationService
from data_service import DataService
from decision_service import DecisionService
from weather_service import WeatherService

import unittest
import automationhat as ah

class EntTest(unittest.TestCase):
	
	def setUp(self):
		
		self.dataService = DataService()
		self.decisionService = DecisionService()
		self.weatherService = WeatherService()
	
	def tearDown(self):
		
		del self.dataService
		del self.decisionService
		del self.weatherService
	
	def test_actuation_service_get_sensor(self):
		
		data = ActuationService.get_sensor()
		self.assertGreater(data, 0.03)
		
	def test_actuation_service_valve_open(self):
		
		ActuationService.valve_open()
		self.assertTrue(ah.relay.one.is_on())
		
	def test_actuation_service_valve_close(self):
		
		ActuationService.valve_close()
		self.assertFalse(ah.relay.one.is_on())
	
	def test_actuation_service_pump_on(self):
		
		ActuationService.pump_on()
		self.assertTrue(ah.output.one.is_on())
	
	def test_actuation_service_pump_off(self):
		
		ActuationService.pump_off()
		self.assertFalse(ah.output.one.is_on())
	
	def test_data_service_write_document(self):
		
	    doc = { "id": "unit-test-key", "value": 0 }
	    result = dataService.write_document(doc)
	    self.assertTrue(result)
	
	def test_decision_service_make_decision(self):
		
		waterContent = 0.0
		rainChance = 0.25
		decision = self.decisionService.make_decision(waterContent, decision)
		self.assertContains([self.decisionService.DO_NOTHING, \
			self.decisionService.DO_WATER, \
			self.decisionService.DO_WATER_AND_FERTILIZER], 
			decision)
	
	def test_weather_service_chance_of_rain(self):
		
		chanceOfRain = self.weatherService.chance_of_rain()
		self.assertGreaterEqual(chanceOfRain, 0.0)

if __name__ == "__main__":
	
	unittest.main()
