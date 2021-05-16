from default_values import WATER_CONTENT, RAIN, FERTILIZER_DAY_ONE_NAME, FERTILIZER_DAY_TWO_NAME

import os, datetime

class DecisionService():
	DO_NOTHING="NO_ACTION"
	DO_WATER="WATER"
	DO_FERTILIZER="FERTILIZE"
	DO_WATER_AND_FERTILIZER="WATER_AND_FERTILIZE"
	
	def __init__(self):
		
		self.waterContentThreshold = os.environ.get("WATER_CONTENT") or WATER_CONTENT
		self.rainThreshold = os.environ.get("RAIN") or RAIN
		self.fertilizingDays = [dayName.upper() for dayName \
			in [os.environ.get("FERTILIZER_DAY_ONE_NAME") or FERTILIZER_DAY_ONE_NAME, \
			os.environ.get("FERTILIZER_DAY_TWO_NAME") or FERTILIZER_DAY_TWO_NAME] if dayName]
	
	def make_decision(self, waterContent: float, chanceOfRain: float) -> int:
		
		dayName = datetime.datetime.now().strftime("%A").upper()
		
		if waterContent >= self.waterContentThreshold \
			and chanceOfRain <= self.rainThreshold:

			if dayName in [d.upper() for d in self.fertilizingDays]:
				return DecisionService.DO_WATER_AND_FERTILIZER
				
			return DecisionService.DO_WATER
		
		elif dayName in self.fertilizingDays:
				return DecisionService.DO_FERTILIZER
		
		return DecisionService.DO_NOTHING
