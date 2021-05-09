import os, datetime

class DecisionService():
	DO_NOTHING=0
	DO_WATER=1
	DO_WATER_AND_FERTILIZER=2
	
	def __init__(self):
		
		self.waterContentThreshold = os.environ.get("WATER_CONTENT")
		self.rainThreshold = os.environ.get("RAIN")
		self.fertilizingDays = [dayName.upper() for dayName \
			in [os.environ.get("FERTILIZER_DAY_ONE_NAME") \
			os.environ.get("FERTILIZER_DAY_TWO_NAME")] if dayName]
	
	def make_decision(self, waterContent: float, chanceOfRain: float) -> int:
		
		if waterContent < self.waterContentThreshold \
			and chanceOfRain < self.rainThreshold:
				
			dayName = datetime.datetime.now().strftime("%A").upper()
			
			if dayName in self.fertilizingDays:
				return DO_WATER_AND_FERTILIZER
				
			return DO_WATER
		
		return DO_NOTHING
