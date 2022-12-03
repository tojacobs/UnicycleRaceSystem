import time
from _thread import start_new_thread

from unittest.mock import Mock

from raceSystem.client import Client
from raceSystem.UnicycleRaceSystem import UnicycleRaceSystem


def test_happyFlowRace():
    # Create the raceSystem with the ui mocked
    raceSystem = UnicycleRaceSystem()
    raceSystem._UIs[0] = Mock()

    # Create the 2 clients
    startClient = Client("StartClient", 0, 0, 0)
    finishClient = Client("FinishClient", 0, 0, 0)

    # Run server and both clients
    start_new_thread(raceSystem.run, ())
    start_new_thread(startClient.runClientProgram, ())
    start_new_thread(finishClient.runClientProgram, ())

    # Wait a couple seconds so everything can connect and start
    time.sleep(5)

    # Assert that start and finish client are both connected
    raceSystem._UIs[0].startClientConnected.assert_called_once()
    raceSystem._UIs[0].finishClientConnected.assert_called_once()

    # Start a raceSequence and wait a bit more than countdown time
    raceSystem.setCountdown(1)
    start_new_thread(raceSystem.startRace, ())
    time.sleep(1.1)

    # Assert that countdown was started and ended
    raceSystem._UIs[0].countDownStarted.assert_called_once()
    raceSystem._UIs[0].countDownEnded.assert_called_once()

    # Trigger startClient signals
    startClient.signalFoundP1(0)
    startClient.signalFoundP2(0)

    # Wait a second and trigger finishClient signals
    time.sleep(1)
    finishClient.signalFoundP1(0)
    finishClient.signalFoundP2(0)

    # Wait a second and assert that race is ended
    time.sleep(1)
    raceSystem._UIs[0].raceEnded.assert_called_once()

    # Next assert the arguments of sendResult for P1 and P2 but first assign id's for readability
    P1 = 0
    P2 = 1
    pId = 0
    falseStartId = 1
    dnfId = 2
    raceTimeid = 3
    reactionTimeId = 4

    # Assert that we are asserting the arguments of P1
    assert P1 is raceSystem._UIs[0].sendResult.call_args_list[P1].args[pId]
    # Assert that falseStart is False
    assert False is raceSystem._UIs[0].sendResult.call_args_list[P1].args[falseStartId]
    # Assert that DNF is False
    assert False is raceSystem._UIs[0].sendResult.call_args_list[P1].args[dnfId]
    # Assert that raceTime is not None
    assert None is not raceSystem._UIs[0].sendResult.call_args_list[P1].args[raceTimeid]
    # Assert that reactionTime is not None
    assert None is not raceSystem._UIs[0].sendResult.call_args_list[P1].args[reactionTimeId]

    # Assert that we are asserting the arguments of P2
    assert P2 is raceSystem._UIs[0].sendResult.call_args_list[P2].args[pId]
    # Assert that falseStart is False
    assert False is raceSystem._UIs[0].sendResult.call_args_list[P2].args[falseStartId]
    # Assert that DNF is False
    assert False is raceSystem._UIs[0].sendResult.call_args_list[P2].args[dnfId]
    # Assert that raceTime is not None
    assert None is not raceSystem._UIs[0].sendResult.call_args_list[P2].args[raceTimeid]
    # Assert that reactionTime is not None
    assert None is not raceSystem._UIs[0].sendResult.call_args_list[P1].args[reactionTimeId]
