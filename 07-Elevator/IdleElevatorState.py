from ElevatorState import ElevatorState

class IdleElevatorState(ElevatorState):
    
    def goUpPushedFromFloor(self, floor):
        print "go"