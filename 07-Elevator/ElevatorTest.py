# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest

from State import State

from CabinState import CabinState
from CabinDoorState import CabinDoorState
from ElevatorState import ElevatorState

from StoppedCabinState import StoppedCabinState
from MovingCabinState import MovingCabinState

from IdleElevatorState import IdleElevatorState
from WorkingElevatorState import WorkingElevatorState

from OpenedCabinDoorState import OpenedCabinDoorState
from ClosedCabinDoorState import ClosedCabinDoorState
from OpeningCabinDoorState import OpeningCabinDoorState
from ClosingCabinDoorState import ClosingCabinDoorState


from enum import Enum

floorToGoStack = []
class ElevatorState(Enum):
    IDLE = 1
    WORKING = 2

class CabinState(Enum):
    STOPPED = 1
    MOVING = 2

class CabinDoorState(Enum):
    OPENED = 1
    OPENING = 2
    CLOSING = 3
    CLOSED = 4

class ElevatorController:
    def __init__(self):
        self.state = ElevatorState.IDLE
        self.cabin_state = CabinState.STOPPED
        self.cabin_door_state = CabinDoorState.OPENED
        self.cabin_floor_number = 0
    
    def isIdle(self):
        return self.state is ElevatorState.IDLE
    
    def isWorking(self):
        return self.state is ElevatorState.WORKING
    
    def isCabinStopped(self):
        return self.cabin_state is CabinState.STOPPED
    
    def isCabinMoving(self):
        return self.cabin_state is CabinState.MOVING

    def isCabinWaitingForPeople(self):
        return self.cabin_state is CabinState.STOPPED
    
    def isCabinDoorOpened(self):
        return self.cabin_door_state is CabinDoorState.OPENED
    
    def isCabinDoorOpening(self):
        return self.cabin_door_state is CabinDoorState.OPENING

    def isCabinDoorClosing(self):
        return self.cabin_door_state is CabinDoorState.CLOSING
    
    def isCabinDoorClosed(self):
        return self.cabin_door_state is CabinDoorState.CLOSED

    def cabinFloorNumber(self):
        return self.cabin_floor_number

    def goUpPushedFromFloor(self, floor):
        if self.isIdle():
            self.state = ElevatorState.WORKING
            self.cabin_door_state = CabinDoorState.CLOSING
        else :
            floorToGoStack.append(floor)

    def cabinDoorClosed(self):
        if self.isCabinDoorOpened() or self.isCabinDoorOpening() or self.isCabinDoorClosed():
           raise ElevatorEmergency("Sensor de puerta desincronizado")

        self.cabin_state = CabinState.MOVING
        self.cabin_door_state = CabinDoorState.CLOSED
        
    def cabinOnFloor(self, floor):
        if self.isCabinStopped() or abs(self.cabin_floor_number - floor) > 1 :
           raise ElevatorEmergency("Sensor de cabina desincronizado")
        self.cabin_state = CabinState.STOPPED
        self.cabin_door_state = CabinDoorState.OPENING
        self.cabin_floor_number = floor

    def cabinDoorOpened(self):
        if not floorToGoStack:
            self.state = ElevatorState.IDLE
        else :
            self.state = ElevatorState.WORKING
        self.cabin_door_state = CabinDoorState.OPENED

    def waitForPeopleTimedOut(self):
        self.cabin_door_state = CabinDoorState.CLOSING
    
    def openCabinDoor(self):
        if self.isCabinStopped() and not self.isCabinDoorOpened() or self.isCabinDoorClosing():
            self.cabin_door_state = CabinDoorState.OPENING

    def closeCabinDoor(self):
        if self.isWorking() and not self.isCabinDoorClosed() and not self.isCabinDoorOpening():
            self.cabin_door_state = CabinDoorState.CLOSING

class ElevatorEmergency(Exception):
    def __init__(self, message):
        self.message = message

class ElevatorTest(unittest.TestCase):

    def test01ElevatorStartsIdleWithDoorOpenOnFloorZero(self):
        elevatorController = ElevatorController()
        
        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertEqual(0,elevatorController.cabinFloorNumber())
    
    def test02CabinDoorStartsClosingWhenElevatorGetsCalled(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        
        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())
        
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertTrue(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())
    
    def test03CabinStartsMovingWhenDoorGetsClosed(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        
        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
    
        self.assertFalse(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinMoving())
        
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    
    def test04CabinStopsAndStartsOpeningDoorWhenGetsToDestination(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertFalse(elevatorController.isIdle())
        self.assertTrue(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())
                
        self.assertFalse(elevatorController.isCabinDoorOpened())
        self.assertTrue(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())

        self.assertEqual(1,elevatorController.cabinFloorNumber())
        
    def test05ElevatorGetsIdleWhenDoorGetOpened(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        
        self.assertTrue(elevatorController.isIdle())
        self.assertFalse(elevatorController.isWorking())
        
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertFalse(elevatorController.isCabinMoving())

        self.assertTrue(elevatorController.isCabinDoorOpened())
        self.assertFalse(elevatorController.isCabinDoorOpening())
        self.assertFalse(elevatorController.isCabinDoorClosing())
        self.assertFalse(elevatorController.isCabinDoorClosed())
        
        self.assertEqual(1,elevatorController.cabinFloorNumber())  
    
    def test06DoorKeepsOpenedWhenOpeningIsRequested(self):
        elevatorController = ElevatorController()
        
        self.assertTrue(elevatorController.isCabinDoorOpened())
        
        elevatorController.openCabinDoor()

        self.assertTrue(elevatorController.isCabinDoorOpened())

    def test07DoorMustBeOpenedWhenCabinIsStoppedAndClosingDoors(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())
        
        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

    def test08CanNotOpenDoorWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    
    def test09DoorKeepsOpeneingWhenItIsOpeneing(self):
        elevatorController = ElevatorController()
    
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.openCabinDoor()
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    def test10RequestToGoUpAreEnqueueWhenRequestedWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())
    
    def test11CabinDoorStartClosingAfterWaitingForPeople(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())
    
    def test12StopsWaitingForPeopleIfCloseDoorIsPressed(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorOpened()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinWaitingForPeople())
        self.assertTrue(elevatorController.isCabinDoorOpened())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())

    def test13CloseDoorDoesNothingIfIdle(self):
        elevatorController = ElevatorController()
        
        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isIdle())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpened())

    def test14CloseDoorDoesNothingWhenCabinIsMoving(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinMoving())
        self.assertTrue(elevatorController.isCabinDoorClosed())
    
    def test15CloseDoorDoesNothingWhenOpeningTheDoorToWaitForPeople(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
    
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

        elevatorController.closeCabinDoor()

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())

    def test16ElevatorHasToEnterEmergencyIfStoppedAndOtherFloorSensorTurnsOn(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")

    def test17ElevatorHasToEnterEmergencyIfFalling(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinOnFloor(0)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")

    def test18ElevatorHasToEnterEmergencyIfJumpsFloors(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(3)
        try:
            elevatorController.cabinDoorClosed()
        
            elevatorController.cabinOnFloor(3)
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de cabina desincronizado")
        
    def test19ElevatorHasToEnterEmergencyIfDoorClosesAutomatically(self):
        elevatorController = ElevatorController()
        
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        
    def test20ElevatorHasToEnterEmergencyIfDoorClosedSensorTurnsOnWhenClosed(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        
    

    def test21ElevatorHasToEnterEmergencyIfDoorClosesWhenOpening(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
        try:
            elevatorController.cabinDoorClosed()
            self.fail()
        except ElevatorEmergency as elevatorEmergency:
            self.assertTrue (elevatorEmergency.message == "Sensor de puerta desincronizado")
        
    

    # # STOP HERE!!
    # # More tests here to verify bad sensor function
    
    def test22CabinHasToStopOnTheFloorsOnItsWay(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)

        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test23ElevatorCompletesAllTheRequests(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(2)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test24CabinHasToStopOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorOpening())
    
    
    def test25CabinHasToStopAndWaitForPeopleOnFloorsOnItsWayNoMatterHowTheyWellCalled(self):
        elevatorController = ElevatorController()
        
        elevatorController.goUpPushedFromFloor(2)
        elevatorController.cabinDoorClosed()
        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinOnFloor(1)
        elevatorController.cabinDoorOpened()
        elevatorController.waitForPeopleTimedOut()
        
        self.assertTrue(elevatorController.isWorking())
        self.assertTrue(elevatorController.isCabinStopped())
        self.assertTrue(elevatorController.isCabinDoorClosing())

    
if __name__ == "__main__":
    unittest.main()


