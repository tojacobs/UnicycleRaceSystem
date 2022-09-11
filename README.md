# UnicycleRaceSystem
Time registration system for off road unicycle races

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
