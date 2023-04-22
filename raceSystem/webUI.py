from unicodedata import name
from flask import *
from raceSystem.userInterface import UserInterface
from _thread import *
import time

class WebIU(UserInterface):
    def __init__(self) -> None:
        self._app = Flask(__name__)
        self._startClientConnected = False
        self._finishClientConnected = False


    def homePage(self):
        name1 = self.getNameCallback(0)
        name2 = self.getNameCallback(1)
        if self._startClientConnected:
            sClient = "Connected"
        else:
            sClient = ""
        if self._finishClientConnected:
            fClient = "Connected"
        else:
            fClient = ""
        return render_template("home.html", name_1 = name1 + " ", name_2 = name2 + " ", StartClient = sClient, FinshClient = fClient)

    def run(self):
        """Start the user interface"""
        @self._app.route("/", methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                try:
                    self.setNameCallback(0,request.form['Naam_1'])
                except:
                    return '<p>Baan 1: ongeldige naam</p>'

                try:
                    self.setNameCallback(1,request.form['Naam_2'])
                except:
                    return '<p>Baan 2: ongeldige naam</p>'
            elif request.method == 'GET':
                return self.homePage()
                
            return self.homePage()

        @self._app.route("/raceControl", methods=['POST'])
        def raceControl():
            if request.method == 'POST':
                if request.form.get('btnStart') == 'Start':
                    self.startRaceCallback()
                elif  request.form.get('btnStop') == 'Stop':
                    self.stopRaceCallback()
            return '', 204
        
        @self._app.route("/setNames", methods=['POST', 'GET'])
        def setNames():
            if request.method == 'POST':
                self.setNameCallback(0,request.form.get('Naam_1'))
                self.setNameCallback(1,request.form.get('Naam_2'))

            name1 = self.getNameCallback(0)
            name2 = self.getNameCallback(1)
            
            return render_template("home.html", name_1 = name1 + " ", name_2 = name2 + " ")

        @self._app.route('/settings',methods = ['POST', 'GET'])
        def settings():
            if request.method == 'POST':
                try:
                    countdown = int(request.form['countdown'])
                except:
                    return "<p>Countdown: ongeldige waarde</p>"

                try:
                    orange = int(request.form['orange'])
                except:
                    return "<p>Oranje: ongeldige waarde</p>"

                if orange >= countdown:
                    return "<p>Oranje: waarde moet lager zijn dan countdown</p>"

                self.setCountdownCallback(countdown)
                self.setOrangeLightAtCallback(orange)
            
                return render_template("settings.html",countdownValue=countdown, orangeValue=orange)
            else:
                countdown = self.getCountdownCallback()
                orange = self.getOrangeLightAtCallback()
                return render_template("settings.html",countdownValue=countdown, orangeValue=orange)
                pass

        @self._app.route('/get-status')
        def getStatus():
            print(self._startClientConnected)
            print(self._finishClientConnected)
            return jsonify(xStartClientConnected=self._startClientConnected, xFinishClientConnected=self._finishClientConnected)

        self._app.run(debug=True, use_reloader=False)

    def setCallbackFunctions(self, exitCallback, startRaceCallback, stopRaceCallback, setNameCallback, getNameCallback,
                             setCountdownCallback, getCountdownCallback, setOrangeLightAtCallback, getOrangeLightAtCallback,
                             setResetTimerSeconds, getResetTimerSeconds):
        self.exitCallback             = exitCallback
        self.startRaceCallback        = startRaceCallback
        self.stopRaceCallback         = stopRaceCallback
        self.setNameCallback          = setNameCallback
        self.getNameCallback          = getNameCallback
        self.setCountdownCallback     = setCountdownCallback
        self.getCountdownCallback     = getCountdownCallback
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
        pass
    def countDownEnded(self):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def raceEnded(self, winner):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def sendResult(self, index:int, falseStart:bool, DNF:bool, raceTime:tuple, reactionTimeMs:int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def startSignalDetected(self, index:int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def finishSignalDetected(self, index:int):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass
    def falseStartDetected(self, index):
        """Callback function that will be called from UnicycleRaceSystem"""
        pass