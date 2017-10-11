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


class ContextStates():
    
    def __init__(self):
        self.cabin_door_state = OpenedCabinDoorState()
        self.state = IdleElevatorState()
        self.cabin_state = StoppedCabinState()
    
    def getElevatorState(self):
        return self.state

    def getCabinDoorState(self):
        return self.cabin_door_state

    def getCabinState(self):
        return self.cabin_state

    def setElevatorState(self, elevatorState):
        self.state = elevatorState
    
    def setCabinDoorState(self, cabinDoorState):
        self.cabin_door_state = cabinDoorState
    
    def setCabinState(self, cabinState):
        self.cabin_state = cabinState
    
