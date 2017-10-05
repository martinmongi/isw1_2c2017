from CabinState import CabinState

class StoppedCabinState(CabinState):
    def openCabinDoor(self):
        print 'openDoor'