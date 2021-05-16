from actuation_service import ActuationService
from data_service import DataService
from decision_service import DecisionService
from default_values import CLOUD_ENABLED
from display_service import DisplayService
from weather_service import WeatherService
from datetime import datetime
from json import dumps
from time import sleep

import os

if __name__ == "__main__":
	
	now = datetime.now()
	
	logDir = "/home/pi/Ent/logs"
	logPath = logDir + "/"  + now.strftime("%m-%d-%Y-%H-%M-%S") + ".json"
	
	document = {
		"date": now.strftime("%m/%d/%Y, %H:%M:%S"),
		"waterContent": 0.0,
		"chanceOfRain": 0.0,
		"decision": "n/a",
		"logPath": logPath,
		"serviceError": None,
		"databaseError": None}
		
	print("1")
	
	try:
		
		waterContent = ActuationService.get_sensor()
		
		print("2")
		
		weather = WeatherService()
		chanceOfRain = weather.chance_of_rain()
		decision = DecisionService()
		
		print("3")
		
		action = decision.make_decision(waterContent, chanceOfRain)
		display = DisplayService()
		display.draw_analog_values()
		
		print("4")
		
		actuationService = ActuationService(display=display)
		
		print("5")
		
		if action == decision.DO_WATER:
			actuationService.water()
			display.draw_output_states()
			
		elif action == decision.DO_FERTILIZER:
			actuationService.fertilize()
			display.draw_output_states()
			
		elif action == decision.DO_WATER_AND_FERTILIZER:
			actuationService.water_and_fertilize()
			display.draw_output_states()
		
		print("6")
		
		document["waterContent"] = waterContent
		document["chanceOfRain"] = chanceOfRain
		document["decision"] = action
		
	except Exception as ex:
		print(ex)
		document["serviceError"] = str(ex)
	
	if(CLOUD_ENABLED):
		try:
			
			data = DataService()
			data.write_document(document)
			
		except Exception as ex:
			
			document["databaseError"] = str(ex)
			
	print("7")
	
	if not os.path.exists(logDir): os.makedirs(logDir)
	with open(logPath, "w+") as f: f.write(dumps(document))
	
	print("8")
