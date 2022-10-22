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
    # Act
    racer.countDownStarted()

    # Assert
    racer._light.turnOn.assert_called_once_with(Color.Red)


def test_switchToOrangeLightStatus(racer):
    '''Test if after switchToOrange is called red light is turned off and orange turned on'''
    # Act
    racer.swithToOrange()

    # Assert
    racer._light.turnOff.assert_called_once_with(Color.Red)
    racer._light.turnOn.assert_called_once_with(Color.Orange)


def test_startRaceLightStatus(racer):
    '''Test if after startRace is called red and orange light is turned off and green turned on'''
    # Arrange
    expectedCalls = [call.turnOn(Color.Green), call.turnOff(Color.Red), call.turnOff(Color.Orange)]

    # Act
    racer.startRace()

    # Assert
    racer._light.assert_has_calls(expectedCalls, any_order=True)


def test_startRaceLightStatusFalseStart(racer):
    '''Test if after startRace is called when there was a false start turnOff and turnOn are not called
    because the light status should stay as is. But setBlinking is is called which will let the turned on light blink'''
    # Arrange
    racer.setFalseStart(True)

    # Act
    racer.startRace()

    # Assert
    racer._light.turnOff.assert_not_called()
    racer._light.turnOn.assert_not_called()
    racer._light.setBlinking.assert_called_once_with(True)


def test_setFunctions(racer):
    '''Test if all the set and the "dumb" get funtions work properly'''
    # Arrange
    name = "Tom"
    startTime = 1
    finishTime = 2
    reactionTime = 3
    falseStart = True
    racer.setName(name)
    racer.setStartTime(startTime)
    racer.setFinishTime(finishTime)
    racer.setReactionTime(reactionTime)
    racer.setFalseStart(falseStart)
    racer.setDNF()

    # Act and Assert
    assert name is racer.getName()
    assert startTime is racer._startTimeInMs
    assert finishTime is racer._finishTimeInMs
    assert reactionTime is racer._startLineTimeInMs
    assert falseStart is racer.getFalseStart()
    assert True is racer.getDNF()
    assert True is racer.getFinished()


def test_resetFunction(racer):
    '''Test if calling reset actually resets all the required paramaters and the trafficlight'''
    # Arrange
    startTime = 1
    finishTime = 2
    reactionTime = 3
    falseStart = True
    racer.setStartTime(startTime)
    racer.setFinishTime(finishTime)
    racer.setReactionTime(reactionTime)
    racer.setFalseStart(falseStart)
    racer.setDNF()
    expectedCalls = [call.turnOff(Color.Green), call.turnOff(Color.Red), call.turnOff(Color.Orange), call.setBlinking(False)]

    # Act
    racer.reset()

    # Assert
    assert None is racer._startTimeInMs
    assert None is racer._finishTimeInMs
    assert None is racer._startLineTimeInMs
    assert False is racer.getFalseStart()
    assert False is racer.getDNF()
    assert False is racer.getFinished()
    racer._light.assert_has_calls(expectedCalls, any_order=True)


def test_getReactionTimeNoStartLineTime(racer):
    '''Test that getReactionTimeInMs returns None if startLineTimeInMs was not set'''
    # Act and Assert
    assert None is racer.getReactionTimeInMS()


def test_getReactionTimeNoStartTime(racer):
    '''Test that getReactionTimeInMs returns TypeError if startTime was not set
    The rationale is that if this happens the Racer object is being used wrong and an error should be thrown'''
    # Arrange
    racer.setReactionTime(1)

    # Act and Assert
    with pytest.raises(TypeError):
        racer.getReactionTimeInMS()


def test_getReactionTimeCalculation(racer):
    '''Test the calculation of getReactionTimeInMs with a 150ms positive result rounded to ms'''
    # Arrange
    racer.setStartTime(1666463721.5420716)
    racer.setReactionTime(1666463721.6920999)
    expectedReactionTimeInMs = 150

    # Act and Assert
    assert expectedReactionTimeInMs == racer.getReactionTimeInMS()


def test_getReactionTimeCalculationNegative(racer):
    '''Test the calculation of getReactionTimeInMs with a -5ms negative result rounded to ms'''
    # Arrange
    racer.setStartTime(1666463721.5420716)
    racer.setReactionTime(1666463721.5360000)
    expectedReactionTimeInMs = -6

    # Act and Assert
    assert expectedReactionTimeInMs == racer.getReactionTimeInMS()


def test_getRaceTimeWithDnf(racer):
    '''Test that getRaceTime returns (0, 0) when DNF is True'''
    # Arrange
    racer.setDNF()

    # Act and Assert
    assert (0, 0) == racer.getRaceTime()


def test_getRaceTimeCalculationUnder1Minute(racer):
    '''Test that getRaceTime returns 0.75 minutes and 45 seconds when the time diff is 45 seconds'''
    # Arrange
    startTime = 1666463721.5420716
    finishTime = 1666463766.5420716
    racer.setStartTime(startTime)
    racer.setFinishTime(finishTime)

    # Act and Assert
    assert (0.75, 45.0) == racer.getRaceTime()


def test_getRaceTimeCalculationOver1Minute(racer):
    '''Test that getRaceTime returns 2.25 minutes and 15 seconds when the time diff is 135 seconds'''
    # Arrange
    startTime = 1666463721.5420716
    finishTime = 1666463856.5420716
    racer.setStartTime(startTime)
    racer.setFinishTime(finishTime)

    # Act and Assert
    assert (2.25, 15.0) == racer.getRaceTime()


def test_getRaceTimeNoFinishTime(racer):
    '''Test that getRaceTime returns TypeError if finishTime was not set
    The rationale is that if this happens the Racer object is being used wrong and an error should be thrown'''
    # Arrange
    startTime = 1666463721.5420716
    racer.setStartTime(startTime)

    # Act and Assert
    with pytest.raises(TypeError):
        racer.getRaceTime()


def test_getRaceTimeNoStartTime(racer):
    '''Test that getRaceTime returns TypeError if startTime was not set
    The rationale is that if this happens the Racer object is being used wrong and an error should be thrown'''
    # Arrange
    finishTime = 1666463721.5420716
    racer.setFinishTime(finishTime)

    # Act and Assert
    with pytest.raises(TypeError):
        racer.getRaceTime()
