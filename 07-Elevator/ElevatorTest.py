# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest

class ElevatorState():

    def __init__(self, context):
        self.context = context
    def goUpPushedFromFloor(self, floor):
        pass
    def closeCabinDoorWhenDoorisOponed(self):
        pass
class IdleElevatorState(ElevatorState):
    
    def goUpPushedFromFloor(self, floor):
        self.context.state = WorkingElevatorState(self.context)
        self.context.cabin_door_state = ClosingCabinDoorState(self.context)

class WorkingElevatorState(ElevatorState):
    def goUpPushedFromFloor(self, floor):
        self.context.floorToGoStack.append(floor)
    def closeCabinDoorWhenDoorisOponed(self):
        self.context.cabin_door_state = ClosingCabinDoorState(self.context)
class CabinState():
    
    def __init__(self, context):
        self.context = context


    def openCabinDoorWhenDoorIsOpened(self):
        pass
class StoppedCabinState(CabinState):
    def cabinOnFloor(self, floor):
       raise ElevatorEmergency("Sensor de cabina desincronizado")
    def openCabinDoorWhenDoorIsOpened():
        self.context.cabin_door_state = OpeningCabinDoorState(self.context)

class MovingCabinState(CabinState):

    def cabinOnFloor(self, floor):       
        if  abs(self.context.cabin_floor_number - floor) > 1 :
            raise ElevatorEmergency("Sensor de cabina desincronizado")
        self.context.cabin_state = StoppedCabinState(self.context)
        self.context.cabin_floor_number = floor
        self.context.cabin_door_state = OpeningCabinDoorState(self.context)

class CabinDoorState():

    def __init__(self, context):
        self.context = context
    def openCabinDoor(self):
        pass
    def closeCabinDoor(self):
        pass
class OpeningCabinDoorState(CabinDoorState):
    def cabinDoorClosed(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")
class OpenedCabinDoorState(CabinDoorState):
    def cabinDoorClosed(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")
    def closeCabinDoor(self):
        self.context.state.closeCabinDoorWhenDoorisOponed()
class ClosingCabinDoorState(CabinDoorState):
    def cabinDoorClosed(self):
        self.context.cabin_state = MovingCabinState(self.context)
        self.context.cabin_door_state = ClosedCabinDoorState(self.context)
    def openCabinDoor(self):
        self.context.cabin_door_state = OpeningCabinDoorState(self.context)
class ClosedCabinDoorState(CabinDoorState):
    def cabinDoorClosed(self):
        raise ElevatorEmergency("Sensor de puerta desincronizado")
    def openCabinDoor(self):
        self.context.cabin_state.openCabinDoorWhenDoorIsOpened()
class ContextStates():
    def __init__(self):
        self.cabin_door_state = OpenedCabinDoorState(self)
        self.state = IdleElevatorState(self)
        self.cabin_state = StoppedCabinState(self)
        self.floorToGoStack = []
        self.cabin_floor_number = 0
class ElevatorController:
    
    def __init__(self):
        self.context = ContextStates()
    def isIdle(self):
        return isinstance(self.context.state, IdleElevatorState)
    
    def isWorking(self):
        return isinstance(self.context.state, WorkingElevatorState)
    
    def isCabinStopped(self):
        return isinstance(self.context.cabin_state, StoppedCabinState)
    
    def isCabinMoving(self):
        return isinstance(self.context.cabin_state, MovingCabinState)

    def isCabinWaitingForPeople(self):
        return self.isCabinStopped()
    
    def isCabinDoorOpened(self):
        return isinstance(self.context.cabin_door_state, OpenedCabinDoorState)
    
    def isCabinDoorOpening(self):
        return isinstance(self.context.cabin_door_state, OpeningCabinDoorState)

    def isCabinDoorClosing(self):
        return isinstance(self.context.cabin_door_state, ClosingCabinDoorState)
    
    def isCabinDoorClosed(self):
        return isinstance(self.context.cabin_door_state, ClosedCabinDoorState)

    def cabinFloorNumber(self):
        return self.context.cabin_floor_number

    def goUpPushedFromFloor(self, floor):
        self.context.state.goUpPushedFromFloor(floor)
        # if self.isIdle():
        #     self.state = WorkingElevatorState()
        #     self.cabin_door_state = ClosingCabinDoorState()
        # else :
        #     self.floorToGoStack.append(floor)

    def cabinDoorClosed(self):
        self.context.cabin_door_state.cabinDoorClosed()

        # if self.isCabinDoorOpened() or self.isCabinDoorOpening() or self.isCabinDoorClosed():
        #    raise ElevatorEmergency("Sensor de puerta desincronizado")

        # self.cabin_state = MovingCabinState()
        # self.cabin_door_state = ClosedCabinDoorState()
        
    def cabinOnFloor(self, floor):
        self.context.cabin_state.cabinOnFloor(floor)

        # if self.isCabinStopped() or abs(self.cabinFloorNumber() - floor) > 1 :
        #    raise ElevatorEmergency("Sensor de cabina desincronizado")
        # self.context.cabin_state = StoppedCabinState(self.context)
        # self.context.cabin_door_state = OpeningCabinDoorState(self.context)
        # self.context.cabin_floor_number = floor

    def cabinDoorOpened(self):
        self.context.cabin_door_state = OpenedCabinDoorState(self.context)
        if not self.context.floorToGoStack:
            self.context.state = IdleElevatorState(self.context)
        else :
            self.context.state = WorkingElevatorState(self.context)

    def waitForPeopleTimedOut(self):
        self.context.cabin_door_state = ClosingCabinDoorState(self.context)
    
    def openCabinDoor(self):
        self.context.cabin_door_state.openCabinDoor()
        # if self.isCabinStopped() and not self.isCabinDoorOpened() or self.isCabinDoorClosing(): 
        #     self.context.cabin_door_state = OpeningCabinDoorState(self.context)

    def closeCabinDoor(self):
        self.context.cabin_door_state.closeCabinDoor()
        # if self.isWorking() and not self.isCabinDoorClosed() and not self.isCabinDoorOpening():
        #     self.context.cabin_door_state = ClosingCabinDoorState(self.context)

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


