import os

# DisplayService configs
IMAGES_PATH= os.environ.get("IMAGES_PATH") or "/home/pi/Ent/src/images"

# ActuationService configs
FERTILIZE_TIME_SECONDS=5
WATER_TIME_SECONDS=5

# DecisionService configs
WATER_CONTENT=2.2
RAIN=0.4
FERTILIZER_DAY_ONE_NAME="SATURDAY"
FERTILIZER_DAY_TWO_NAME="TUESDAY"

# WeatherService configs
LAT=38.94491
LONG=-77.14416
OMW_KEY=None

# DataService configs
CDB_URI=None
CDB_KEY=None
CDB_DATABASE=None
CDB_CONTAINER=None
CDB_PKEY=None

# Switch used in test.py and main.py
CLOUD_ENABLED = ((os.environ.get("CDB_URI") or CDB_URI) 
	and (os.environ.get("CDB_KEY") or CDB_KEY)
	and (os.environ.get("CDB_DATABASE") or CDB_DATABASE)
	and (os.environ.get("CDB_CONTAINER") or CDB_CONTAINER)
	and (os.environ.get("CDB_PKEY") or CDB_PKEY))

# Switch used in test.py
WEATHER_ENABLED = ((os.environ.get("LAT") or LAT) 
	and (os.environ.get("LONG") or LONG) 
	and (os.environ.get("OMW_KEY") or OMW_KEY))

# Switch used in test.py
DECISION_ENABLED = (WEATHER_ENABLED 
	and (os.environ.get("WATER_CONTENT") or WATER_CONTENT) 
	and (os.environ.get("RAIN") or RAIN))
