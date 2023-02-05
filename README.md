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

Download the [zip with source code](https://github.com/tojacobs/UnicycleRaceSystem/archive/refs/heads/main.zip) extract it and copy it to the RPi's.
Use the terminal to navigate to the directory on the RPi and run "pip install -e ."

client_config.txt is being used to configure the client RPi's and has to be placed in the same directory as the client.py file (UnicycleRaceSystem-main/raceSystem), inside the client_config.txt you'll find the following information:
```c
    [Client]
    client_type = start
    gpio_in_p1 = 2
    gpio_in_p2 = 3
    server_ip = 192.168.1.173
```
- client_type: start or finish, to indicita whether the clien is a start or finish client
- gpio_in_p1:  The gpio pin used for detection (start or finish) for P1
- gpio_in_p2:  The gpio pin used for detection (start or finish) for P2
- server_ip:   The ip adress of the Server RPi

The programs should be started in the terminal from the raceSystem directory:
In the Server RPi run "sudo python UnicycleRaceSystem.py".
In the client RPi's run "sudo python client.py".
The order of starting doesn't matter.

After server.py is started the program will wait for connection with both clients. A help text with commands will be printer after both are connected, it should be clear from the help text how to continue from this.

Good to know:
- If the server looses connection with one of the clients, it will be displayed and the program will go into connection mode to wait untill the both clients are connected again.
- If the server program is exited while the clients are still running, they will go in connection mode and automatically connect once the server is started again.

## How to run the system on Raspberry Pi's (in Dutch)

Download de [zip met de broncode](https://github.com/tojacobs/UnicycleRaceSystem/archive/refs/heads/main.zip) pak deze uit en zet de uitgepakte map op de RPi's.
Navigeer naar de map op de RPi en run "pip install -e ."

client_config.txt wordt gebruikt door de client RPi's om de configuratie uit te halen en moet in dezelfde directory staan als de client.py file (UnicycleRaceSystem-main/raceSystem), de client_config.txt file ziet er als volgt uit:
```c
    [Client]
    client_type = start
    gpio_in_p1 = 2
    gpio_in_p2 = 3
    server_ip = 192.168.1.173
```
- client_type: Zet hier start of finish in zodat client.py weet of hij de valse start detectie of finish detectie is
- gpio_in_p1:  De gpio pin die wordt gebruikt voor detectie (start of finish) voor P1
- gpio_in_p2:  De gpio pin die wordt gebruikt voor detectie (start of finish) voor P2
- server_ip:   Het ip adres van de pi waarop server.py draait

De programma's dienen opgestart te worden vanuit de terminal in de raceSystem map:
In de server RPi "sudo python UnicycleRaceSystem.py".
In de client RPi's "sudo python client.py".
Volgorde van opstarten maakt niet uit.

Na het opstarten van server.py zal hij wachten op connectie met de clients, als beide clients connected zijn wordt er een helptekst weergegeven op het scherm met mogelijke commando's vanaf hier moet alles zich vanzelf wijzen.

Good to know:
- als server connectie verliest met 1 van de client wordt dit weergegeven en gewacht tot er weer connectie is.
- als server.py wordt afgesloten (ctr+c of exit typen) en de clients nog draaien dan zullen deze automatisch opnieuw connecten als de server weer opgestart is.
