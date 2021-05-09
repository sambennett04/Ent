from time import sleep
import automationhat as ah

class ActuationService():
	
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

if __name__ == "__main__":
	
	print("sensor reading", ActuationService.get_sensor())
	
	
