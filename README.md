# UnicycleRaceSystem
Time registration system for off road unicycle races

De volgende bestanden moeten op de stoplicht pi worden gezet op dezelfde locatie:
- server.py
- racer.py
- trafficLight.py
- state.py

De pi voor valse start detectie:
- startClient.py

De pi voor finish detectie:
- finishClient.py


In startClient.py en finishClient.py:
1. Op regel 83 t/m 87 zie je de volgende code:
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(2, GPIO.RISING, callback=singal_found_p1, bouncetime=200)
    GPIO.add_event_detect(3, GPIO.RISING, callback=singal_found_p2, bouncetime=200)
   Vervang de 2 voor de GPIO pin die gebruikt wordt voor racer p1 en de 3 voor racer p2

Vervolgens kunnen de server.py, startClient.py en finishClient.py opgestart worden.
Doe dit als admin anders werken de GPIO's niet. Je kan inloggen als admin door 'sudo su' of 'sudo pi' te typen in de terminal en het wachtwoord voor de admin in te geven.
Ook kan je 'sudo' voor het uit te voeren commando zetten. Start de programma's vanuit de terminal:
In de stoplicht pi 'python server.py' hetzelfde geld voor de sndere pi's maar daar is het 'python startClient.py'  en 'python finishClient.py'.
Volgorde van opstarten maakt niet uit, wel wordt aangeraden bij het afsluiten om eerst de clients af te sluiten (ctr+c) omdat als je eerst de server afsluit je even 1 a 2 minuten moet wachten voor je deze weer kan opstarten.

Na het opstarten van server.py zal hij wachten op connectie met de clients, als beide clients connected zijn wordt er een helptekst weergegeven op het scherm met mogelijke commando's vanaf hier moet alles zich vanzelf wijzen.

Good to know:
- als server connectie verliest met 1 van de client wordt dit weergegeven en gewacht tot er weer connectie is.
- als server.py wordt afgesloten (ctr+c of exit typen) en de clients nog draaien is er in princiepe niets aan de hand. Maar als dan server.py opnieuw wordt gestart moet bij de clients minimaal 3x een input signaal getriggered worden voordat ze weer connectie kunnen maken met server.py.
