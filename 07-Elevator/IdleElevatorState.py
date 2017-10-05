from ElevatorState import ElevatorState

class IdleElevatorState(ElevatorState):
    def openCabinDoor(self):
        print 'openDoor'
