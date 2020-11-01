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

cd Source

# test for CosmosHelper.py
echo "\n*** TESTING CosmosHelper.py ***\n"
python3 ./CosmosHelper.py

# test for DarkSkyApiHelper.py
echo "\n*** TESTING DarkSkyApiHelper.py ***\n"
python3 ./DarkSkyApiHelper.py

# test for MegaioHelper.py
echo "\n*** TESTING MegaioHelper.py ***\n"
python3 ./MegaioHelper.py

# test for TelemetryHelper.py
echo "\n*** TESTING TelemetryHelper.py ***\n"
python3 ./TelemetryHelper.py

# test for WateringDecisionMaker.py
echo "\n*** TESTING WaterDecisionMaker.py ***\n"
python3 ./WateringDecisionMaker.py
