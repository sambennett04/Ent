from actuation_service import ActuationService
from data_service import DataService
from decision_service import DecisionService
from display_service import DisplayService
from weather_service import WeatherService

from datetime import date
from json import dumps

if __name__ == "__main__":
	
	document = {
		"date": date.today().strftime("%m/%d/%Y, %H:%M:%S"),
		"waterContent": 0.0,
		"chanceOfRain": 0.0,
		"decision": 0,
		"serviceError": None,
		"databaseError": None}
	
	try:
    
		waterContent = ActuationService.get_sensor()
		
		weather = WeatherService()
		chanceOfRain = weather.chance_of_rain()
		
		decision = DecisionService()
		action = decision.make_decision(waterContent, chanceOfRain)
		
		display = DisplayService()
		display.draw_analog_values()
		
		if action == decision.DO_WATER:
			
			ActuationService.valve_open()
			time.sleep(100)
			display.draw_output_states()
			ActuationService.valve_close()
			
		elif action == decision.DO_WATER_AND_FERTILIZER:
			
			ActuationService.valve_open()
			ActuationService.pump_on()
			time.sleep(100)
			ActuationService.pump_off()
			display.draw_output_states()
			ActuationService.valve_close()
		
		document["waterContent"] = waterContent
		document["chanceOfRain"] = chanceOfRain
		document["decision"] = action 
	
	except Exception as ex:
		
		document["serviceError"] = str(ex)
	
	try:
		
		data = DataService()
		data.write_document(document)
		
	except Exception as ex:
		
		document["databaseError"] = str(ex)
		
	logPath = "~/Ent/logs/" + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".json"
	
	with open(logPath) as f:
		
		f.write(dumps(document))
