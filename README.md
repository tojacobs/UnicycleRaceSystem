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
For the RPi's to be able to synchronize their clocks PTPd must be installed, make sure the RPi's have a connection to internet and run "pip install ptpd". For the rest of the steps or running the system a connection to internet is NOT required.

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
Om de tijd op de RPi's te synchronizeren is PTPd nodig, zorg ervoor dat de RPi's verbonden zijn met internet en voer het volgende commondo uit op iederen RPi "pip install ptpd". Voor de rest van de steppen en het draaien van het systeem is geen verbinding met internet nodig.

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

## How to run the system on Windows/Linux for testing purposes

Make sure that [python](https://www.python.org/downloads/) (minimum version 3.6) is installed on your system and be sure to check both check marks at the bottem of the screenshot.

![python](https://user-images.githubusercontent.com/25977592/216842764-970be332-f630-4b3e-87fc-e8c62e5347c4.png)

After the installation open the terminal or windows powershell and run "pip install pysimplegui".  
On Windows you also need to install pyreadline3 "pip install pyreadline3".

Download the [zip with source code](https://github.com/tojacobs/UnicycleRaceSystem/archive/refs/heads/main.zip) and extract it.  
On Windows: Double click the run_manual_test_windows.bat in the UnicycleRaceSystem-main/tests directory.  
On Linux: Open the UnicycleRaceSystem-main/tests directory in a terminal and run run_manual_test_linux.sh.  
5 windows will pop up, like in the screen recording below where a good weather race sequence is being executed:

https://user-images.githubusercontent.com/25977592/216845608-2929228a-6660-4994-837d-5b7133dce9c3.mp4

## The software architecture

The software design was made with the MVP pattern in mind. UnicycleRaceSystem.py is the entry point of the program and serves as the presenter (or abstraction layer) between UserInterface, Server and RaceSequence.  
This way the classes UserInterface, Server and RaceSequence are completely loose coupled from eachother, which makes it easy to refactor, maintain, test or even swap the classes for others. It even makes it possible to have multiple UI's without the Server or RaceSequence classes being aware of it.

It was chosen not to save the UnicycleRaceSystem instance in the UserInterface, Server and RaceSequence classes because that would allow those classes to call all functions available on the UnicycleRaceSystem instance. This could cause problems when functions are called that were not meant to be called from that class. For example RaceSequence callling exit and shutting down the whole system or Server calling stopRace without UserInterface being aware of it.  
To prevent this it was chosen to use callback functions. In the UnicycleRaceSystem class functions are declared that are used as callback functions. UserInterface, Server and RaceSequence each have a set of these functions that they can use, given to them by the "setCallBackFunctions()" function.  
Take for example the "receivedDataFromServer()" function:  
A handle to this function is send to the Server class by calling the "setCallBackFunctions()" function by UnicycleRaceSystem upon starting the system. The Server instance saves the handle to that function as "receivedDataCallback()" and calls it when it received data from one of the clients. The UnicycleRaceSystem will then call "raceSequence.processReceivedData()".

### Class Diagram
For readability of the class diagram it was chosen not to display the callback functions of UnicycleRacesystem.

![CladdDiagram](https://user-images.githubusercontent.com/25977592/218262803-f02e2bff-b987-4de7-ba2a-5c536a8eedfc.jpg)

In a future refactor iTrafficlight will be discoupled from the Racer class and will instead be controlled by the RaceSequence class. This will be done in order to adhere to the loose coupling, high cohesion and single responsibility principles and use the advantages they bring.

### Sequence Diagrams
To give an idea of the flow of functions calls a few sequence diagrams were made.  

![happyFlowConnectionSequence](https://user-images.githubusercontent.com/25977592/218266283-12266f2a-d7ac-4cf7-9f92-5a2841872686.png)

![startExitSequence](https://user-images.githubusercontent.com/25977592/218266303-21469c39-f1c2-476e-8771-6add26a54c84.png)

![happyFlowRaceSequence](https://user-images.githubusercontent.com/25977592/218266310-f42d9f57-9a46-404a-9c3a-17086f134a03.png)

## Continues Integration

For continues integration Github Actions is used. Each time a Pull request to main is made and when a Pull request to main was merged the pipeline will run.

### Static code checker / Linter
As linter flake8 was chosen which uses pycodestyle, pyflakes and mccabe.  
A check is done on all the possible checks excluding E221 (multiple spaces before operator). if any of the checks fail the pipeline build will fail.  
The maximum code complexity is set to 10 and the maximum line lenght to 127 (Github editor width).

### Unit tests
For unit tests pytest and unittest.mock from the standard python library are used. Classes are tested in isolation, any dependencies are mocked.
At the moment only the class Racer.py has unit tests, the goal is to write unit tests for all classes.

### Integration tests
For Integration tests also pytest and unittest.mock from the standard python library are used (or misused hehe).  
In the integration tests 2 clients and a server are started with all UserInterface elements mocked. The clients will connect to the server so these tests  cover the client socket implementation and the communication between the UnicycleRaceSystem, Server, RaceSequence and Racer classes.  
By calling the UnicycleRaceSystem "startRace()" and clients "singalFound()" functions a happy or unhappy race flow can be created. By asserting the data that is being send to the mocked UserInterface the race result can be checked for correctness.  
At the moment there is only 1 integration test with a happy flow sequence. After all unit tests have been written it will be assessed which integration tests are needed to be added.
