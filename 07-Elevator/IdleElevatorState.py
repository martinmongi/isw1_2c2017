from CabinState import CabinState
from CabinDoorState import CabinDoorState
from ElevatorState import ElevatorState

from StoppedCabinState import StoppedCabinState
from MovingCabinState import MovingCabinState

from WorkingElevatorState import WorkingElevatorState

from OpenedCabinDoorState import OpenedCabinDoorState
from ClosedCabinDoorState import ClosedCabinDoorState
from OpeningCabinDoorState import OpeningCabinDoorState
from ClosingCabinDoorState import ClosingCabinDoorState

class IdleElevatorState(ElevatorState):
    
    def goUpPushedFromFloor(self, floor):
        self.context.state = WorkingElevatorState(self.context)
        self.context.cabin_door_state = ClosingCabinDoorState(self.context)