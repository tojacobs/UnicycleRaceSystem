:: this script must be executed from the Test directory
copy client_config_finish.txt client_config.txt
start call python ../client.py
timeout 1
copy client_config_start.txt client_config.txt
start call python ../client.py
timeout 1
del client_config.txt
start call python ../UnicycleRaceSystem.py
