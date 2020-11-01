:'
    description
    -----------
    - tester for helper files
    - if no errors are outputted to the terminal
      then everything is probably ok
    - this script does not test the Groot.py file

    instructions
    ------------
    - run as root with the following command: sudo bash test.sh
'

# test for CosmosHelper.py
python3 ./Source/CosmosHelper.py

# test for DarkSkyApiHelper.py
python3 ./Source/DarkSkyApiHelper.py

# test for MegaioHelper.py
python3 ./Source/MegaioHelper.py

# test for TelemetryHelper.py
python3 ./Source/TelemetryHelper.py

# test for WateringDecisionMaker.py
python3 ./Source/WateringDecisionMaker.py