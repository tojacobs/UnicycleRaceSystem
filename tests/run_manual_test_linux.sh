# this script must be executed from the Test directory
cp client_config_finish.txt client_config.txt
gnome-terminal -- python ../raceSystem/client.py
sleep 0.1
cp client_config_start.txt client_config.txt
gnome-terminal -- python ../raceSystem/client.py
gnome-terminal -- python ../raceSystem/UnicycleRaceSystem.py
rm client_config.txt
