import pytest
from unittest.mock import Mock
from unittest.mock import call

from raceSystem.Racer import Racer
from raceSystem.trafficLight import Color

@pytest.fixture()
def racer():
    '''Create a new racer object with a new mock for trafficLight'''
    racer = Racer("P1", 0, 0, 0)
    racer._light = Mock()
    return racer

def test_countDownStartedLightStatus(racer):
    '''Test if after countDownStarted is called red light is turned on'''
    # Arrange
    # Act
    racer.countDownStarted()

    # Assert
    racer._light.turnOn.assert_called_once_with(Color.Red)

def test_switchToOrangeLightStatus(racer):
    '''Test if after switchToOrange is called red light is turned off and orange turned on'''
    # Arrange
    # Act
    racer.swithToOrange()

    # Assert
    racer._light.turnOff.assert_called_once_with(Color.Red)
    racer._light.turnOn.assert_called_once_with(Color.Orange)

def test_startRaceLightStatus(racer):
    '''Test if after startRace is called red and orange light is turned off and green turned on'''
    # Arrange
    # Act
    racer.startRace()

    # Assert
    expectedCalls = [call.turnOn(Color.Green), call.turnOff(Color.Red), call.turnOff(Color.Orange)]
    racer._light.assert_has_calls(expectedCalls, any_order=True)