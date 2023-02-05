# UnicycleRaceSystem
This is a time registration system that is being used for off the road motorized unicycle races.

## The system in action


https://user-images.githubusercontent.com/25977592/216837483-07cedbf8-91b6-4362-8520-1f61adebfadd.mp4


## How it works
The system consists out of 3 RPI's (Raspberry Pi's) that communicate wireless with each other.
- A start client, to detect reaction time and false starts.
- A finish client, to detect finish times.
- A server, which holds all intelligence and controls the traffic light.

A laptop is used to connect to the Server RPi (f.e. using Putty) to control the system and view the results.

Once the system is started the RPi's use PTPd (a program based on the Precision Time Protocol) to synchronize their clocks. This was tested on Wifi to have a precision of under 10ms.

The clients are designed to be dumb, when they get an input signel they save the timestamp and send that with their ID to the Server RPi.

The Server RPi has all the intelligence. Once a start race command is given to the Server RPi the countdown will start and it will control the traffic light. From that point on the Server RPi will register reaction times, if the reaction time is negative then false start is registered. Once the finish times are received the Server RPi will determine the winner and display the race results. The maximum race lenght is 15 seconds, if there's no finish time within the race lenght the racer will get a Did Not Finish (DNF).
![UnicycleRaceSystem](https://user-images.githubusercontent.com/25977592/216837506-96f3ac52-bd92-461d-938b-90dc4f2dd586.png)

## How to run the system on Raspberry Pi's

De volgende bestanden moeten op de stoplicht pi worden gezet op dezelfde locatie:
- server.py
- Racer.py
- trafficLight.py
- state.py
- raceSequence.py
- userinterface.py
- terminalUI.py
- UnicycleRaceSystem.py

De pi voor valse start detectie:
- client.py
- client_config.txt

De pi voor finish detectie:
- client.py
- client_config.txt

client_config.txt wordt gebruikt door client.py om de configuratie uit te halen en moet in dezelfde directory staan, de file ziet er als volgt uit:
    [Client]
    client_type = start
    gpio_in_p1 = 2
    gpio_in_p2 = 3
    server_ip = 192.168.1.173
- client_type: Zet hier start of finish in zodat client.py weet of hij de valse start detectie of finish detectie is
- gpio_in_p1:  De gpio pin die wordt gebruikt voor detectie (start of finish) voor P1
- gpio_in_p2:  De gpio pin die wordt gebruikt voor detectie (start of finish) voor P2
- server_ip:   Het ip adres van de pi waarop server.py draait

Vervolgens kunnen de UnicycleRaceSystem.py, client.py programma's opgestart worden.
Doe dit als admin anders werken de GPIO's niet. Je kan inloggen als admin door 'sudo su' of 'sudo pi' te typen in de terminal en het wachtwoord voor de admin in te geven.
Ook kan je 'sudo' voor het uit te voeren commando zetten. Start de programma's vanuit de terminal:
In de stoplicht pi 'python UnicycleRaceSystem.py' hetzelfde geld voor de andere pi's maar daar is het 'python client.py'.
Volgorde van opstarten maakt niet uit.

Na het opstarten van server.py zal hij wachten op connectie met de clients, als beide clients connected zijn wordt er een helptekst weergegeven op het scherm met mogelijke commando's vanaf hier moet alles zich vanzelf wijzen.

Good to know:
- als server connectie verliest met 1 van de client wordt dit weergegeven en gewacht tot er weer connectie is.
- als server.py wordt afgesloten (ctr+c of exit typen) en de clients nog draaien is er in princiepe niets aan de hand. Maar als dan server.py opnieuw wordt gestart moet bij de clients minimaal 3x een input signaal getriggered worden voordat ze weer connectie kunnen maken met server.py.
