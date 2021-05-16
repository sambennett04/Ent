from default_values import FERTILIZE_TIME_SECONDS, WATER_TIME_SECONDS
from time import sleep
from display_service import DisplayService

import automationhat as ah
import os

class ActuationService():
	
	def __init__(self, display=None):
		
		# used to support DI from main
		self.display = display or DisplayService()
		self.fertilizerTime = os.environ.get("FERTILIZE_TIME_SECONDS") or FERTILIZE_TIME_SECONDS
		self.waterTime = os.environ.get("WATER_TIME_SECONDS") or WATER_TIME_SECONDS
	
	@staticmethod
	def get_sensor() -> float:
		
		return ah.analog.one.read()
	
	@staticmethod
	def valve_open() -> None:
		
		ah.relay.one.on()
	
	@staticmethod
	def valve_close() -> None:
		
		ah.relay.one.off()
	
	@staticmethod
	def pump_on() -> None:
		
		ah.output.one.write(1)
	
	@staticmethod
	def pump_off() -> None:
		
		ah.output.one.write(0)
	
	def water(self):
		
		ActuationService.valve_open()
		self.display.draw_output_states()
		sleep(self.waterTime)
		ActuationService.valve_close()
		self.display.draw_output_states()
		
	def fertilize(self):
		
		ActuationService.valve_open()
		ActuationService.pump_on()
		self.display.draw_output_states()
		sleep(self.fertilizerTime)
		ActuationService.pump_off()
		ActuationService.valve_close()
		self.display.draw_output_states()
		
	
	def water_and_fertilize(self):
		
		ActuationService.valve_open()
		ActuationService.pump_on()
		self.display.draw_output_states()
		sleep(self.waterTime)
		ActuationService.pump_off()
		ActuationService.valve_close()
		self.display.draw_output_states()
