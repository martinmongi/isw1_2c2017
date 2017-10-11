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
        self.cabin_door_state = OpenedCabinDoorState(self)
        self.state = IdleElevatorState(self)
        self.cabin_state = StoppedCabinState(self)
    
