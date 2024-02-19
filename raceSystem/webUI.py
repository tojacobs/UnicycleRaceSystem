from flask import Flask, render_template, request, jsonify
from raceSystem.userInterface import UserInterface
from raceSystem.RPiTrafficLight import testMode
import time
from _thread import start_new_thread
import logging

class WebIU(UserInterface):
    def __init__(self) -> None:
        self._app = Flask(__name__)
        self._startClientConnected = False
        self._finishClientConnected = False
        self._raceStatus = ''
        self._raceResult = ['', '']
        self._raceOngoing = False
        self._raceLengthInSec = 15

    def run(self):
        """Start the user interface"""
        self.setupFlaskRouting()
        self.startFlask()

    def setupFlaskRouting(self):
        self.homePage()
        self.formRaceControl()
        self.formNames()
        self.settingsPage()
        self.statusRequest()

    def startFlask(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR) #Reduce Flask logging to only error messages

        port = 80
        if testMode:
            self._app.run(port=port, debug=True, use_reloader=False)
        else:
            self._app.run(host= '192.168.1.173', port=port, debug=True, use_reloader=False)

    def homePage(self):
        @self._app.route("/", methods=['GET', 'POST'])
        def index():
            name1 = self.getNameCallback(0)
            name2 = self.getNameCallback(1)
            return render_template(
                "home.html",
                name_1=name1 + " ",
                name_2=name2 + " ")

    def formRaceControl(self):
        @self._app.route("/raceControl", methods=['POST'])
        def raceControl():
            if request.method == 'POST':
                if request.form.get('btnStart') == 'Start':
                    self._raceOngoing = True
                    self.startRaceCallback()
                elif request.form.get('btnStop') == 'Stop':
                    self.stopRaceCallback()
            return '', 204

    def formNames(self):
        @self._app.route("/setNames", methods=['POST', 'GET'])
        def setNames():
            if request.method == 'POST':
                self.setNameCallback(0, request.form.get('Naam_1'))
                self.setNameCallback(1, request.form.get('Naam_2'))

            return self.homePage()

    def statusRequest(self):
        @self._app.route('/get-status')
        def getStatus():
            return jsonify(
                xStartClientConnected=self._startClientConnected,
                xFinishClientConnected=self._finishClientConnected,
                sRaceStatus=self._raceStatus,
                sRaceResult_1=self._raceResult[0],
                sRaceResult_2=self._raceResult[1])

    def settingsPage(self):
        @self._app.route('/settings', methods=['POST', 'GET'])
        def settings():
            if request.method == 'POST':
                try:
                    countdown = int(request.form['countdown'])
                except ValueError:
                    return "<p>Countdown: ongeldige waarde</p>"

                try:
                    orange = int(request.form['orange'])
                except ValueError:
                    return "<p>Oranje: ongeldige waarde</p>"

                if orange >= countdown:
                    return "<p>Oranje: waarde moet lager zijn dan countdown</p>"

                self.setCountdownCallback(countdown)
                self.setOrangeLightAtCallback(orange)

                return render_template(
                    "settings.html",
                    countdownValue=countdown,
                    orangeValue=orange)
            else:
                countdown = self.getCountdownCallback()
                orange = self.getOrangeLightAtCallback()
                return render_template(
                    "settings.html",
                    countdownValue=countdown,
                    orangeValue=orange)
                pass

    def setCallbackFunctions(
            self,
            exitCallback,
            startRaceCallback,
            stopRaceCallback,
            setNameCallback,
            getNameCallback,
            setCountdownCallback,
            getCountdownCallback,
            setOrangeLightAtCallback,
            getOrangeLightAtCallback,
            setResetTimerSeconds,
            getResetTimerSeconds):
        self.exitCallback = exitCallback
        self.startRaceCallback = startRaceCallback
        self.stopRaceCallback = stopRaceCallback
        self.setNameCallback = setNameCallback
        self.getNameCallback = getNameCallback
        self.setCountdownCallback = setCountdownCallback
        self.getCountdownCallback = getCountdownCallback
        self.setOrangeLightAtCallback = setOrangeLightAtCallback
        self.getOrangeLightAtCallback = getOrangeLightAtCallback
        self.setResetTimerSecondsCallback = setResetTimerSeconds
        self.getResetTimerSecondsCallback = getResetTimerSeconds

    def exit(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def startClientConnected(self):
        self._startClientConnected = True
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def finishClientConnected(self):
        self._finishClientConnected = True
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def startClientLost(self):
        self._startClientConnected = False
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def finishClientLost(self):
        self._finishClientConnected = False
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def countDownStarted(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        self._raceStatus = 'Countdown gestart'
        self._raceResult = ['', '']
        pass

    def countDownEnded(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        self._raceStatus = 'Countdown beëindigd'
        start_new_thread(self.startStopRaceTimer, (self._raceLengthInSec, ))
        pass

    def raceEnded(self, winner):
        """Callback function that will be called from UnicycleRaceSystem"""
        self._raceStatus = 'Race geëindigd. De winnaar is: %s' % winner
        self._raceOngoing = False
        pass

    def sendResult(
            self,
            index: int,
            falseStart: bool,
            DNF: bool,
            raceTime: tuple,
            reactionTimeMs: int):
        if falseStart:
            if DNF:
                self._raceResult[index] = "Reactietijd: %s Ms\nRacetijd: DNF\nValse start" % (reactionTimeMs)
            else:
                minutes, seconds = raceTime
                self._raceResult[index] = "Reactietijd: %s Ms\nRacetijd: %d:%.3f\nValse start" % (reactionTimeMs,
                                                                                                  int(minutes),
                                                                                                  seconds)
        else:
            if DNF:
                self._raceResult[index] = "Reactietijd: %s Ms\nRacetijd: DNF" % (reactionTimeMs)
            else:
                minutes, seconds = raceTime
                self._raceResult[index] = "Reactietijd: %s Ms\nRacetijd: %d:%.3f" % (reactionTimeMs, int(minutes), seconds)

    def startSignalDetected(self, index: int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def finishSignalDetected(self, index: int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def falseStartDetected(self, index):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass

    def startStopRaceTimer(self, t):
        while (t and self._raceOngoing):
            time.sleep(1)
            t -= 1
        if self._raceOngoing:
            self._raceStatus = "Race wordt gestopt vanwege de maximale lengte van %s seconden" % self._raceLengthInSec
            self.stopRaceCallback()
