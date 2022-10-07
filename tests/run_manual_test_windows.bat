:: this script must be executed from the Test directory
copy client_config_finish.txt client_config.txt
start call python ../raceSystem/client.py
timeout 1
copy client_config_start.txt client_config.txt
start call python ../raceSystem/client.py
start call python ../raceSystem/UnicycleRaceSystem.py
del client_config.txt
