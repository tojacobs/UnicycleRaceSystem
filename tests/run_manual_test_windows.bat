:: this script must be executed from the Test directory
cd ../
pip install Flask
pip install pyreadline3
pip install -e .
cd tests/
copy client_config_finish.txt client_config.txt
start call python ../raceSystem/client.py
timeout 2
copy client_config_start.txt client_config.txt
start call python ../raceSystem/client.py
start call python ../raceSystem/UnicycleRaceSystem.py
timeout 2
del client_config.txt