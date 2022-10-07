import sys
import pytest

from raceSystem.Racer import Racer
from trafficLightMock import TrafficLightMock
from raceSystem.trafficLight import Color

def test_countDownStartedLightStatus():
    '''Test if after countDownStarted is called the light have the correct status'''
    # Arrange
    light = TrafficLightMock()
    racer = Racer("P1", 0, 0, 0)
    racer._light = light

    # Act
    racer.countDownStarted()

    # Assert
    assert light._colorStatus[Color.Red] == True
    assert light._colorStatus[Color.Orange] == False
    assert light._colorStatus[Color.Green] == False
