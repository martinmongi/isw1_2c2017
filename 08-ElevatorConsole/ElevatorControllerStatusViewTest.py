#
# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  
import unittest
from ElevatorController import ElevatorController, CabinDoorClosingState, CabinDoorClosedState, CabinMovingState, CabinStoppedState, CabinDoorOpeningState, CabinState, CabinDoorState

class ElevatorControllerConsole:
    def __init__(self,elevatorController):
        self._controller = elevatorController
        self._lines = []
        self._controller.acceptVisitor(self)
        self._stateToString = {
            CabinDoorClosingState : "Puerta Cerrandose",
            CabinDoorClosedState : "Puerta Cerrada",
            CabinMovingState : "Cabina Moviendose",
            CabinStoppedState : "Cabina Detenida",
            CabinDoorOpeningState : "Puerta Abriendose"
            }

    def visit(self, aState):
        self._lines.append(self._stateToString[aState])
        
    def lines(self):
        return self._lines

class ElevatorControllerStatusView:
    def __init__(self,elevatorController):
        self._controller = elevatorController
        self._controller.acceptVisitor(self)
        self._doorState = None
        self._cabinState = None
        self._cabinStateToString = {CabinStoppedState : "Stopped"}
        self._doorStateToString = {CabinDoorOpeningState : "Opening"}
    
    def visit(self, aState):
        def updateCabinState(aState):
            self._cabinState = aState
        def updateDoorState(aState):
            self._doorState = aState
        typeIdentifier = {CabinState : updateCabinState, CabinDoorState : updateDoorState}
        typeIdentifier[aState.__bases__[0]](aState)

    def cabinStateFieldModel(self):
        return self._cabinStateToString[self._cabinState]
    
    def cabinDoorStateFieldModel(self):
        return self._doorStateToString[self._doorState]
        
class ElevatorControllerViewTest(unittest.TestCase):
    
    def test01ElevatorControllerConsoleTracksDoorClosingState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        
        elevatorController.goUpPushedFromFloor(1) 
                
        lines = elevatorControllerConsole.lines()

        self.assertEquals(1,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])

    def test02ElevatorControllerConsoleTracksCabinState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        
        elevatorController.goUpPushedFromFloor(1) 
        elevatorController.cabinDoorClosed()
                
        lines = elevatorControllerConsole.lines()

        self.assertEquals(3,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])

    def test03ElevatorControllerConsoleTracksCabinAndDoorStateChanges(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        
        elevatorController.goUpPushedFromFloor(1) 
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
                
        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

    def test04ElevatorControllerCanHaveMoreThanOneView(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        elevatorControllerStatusView = ElevatorControllerStatusView(elevatorController)
        
        elevatorController.goUpPushedFromFloor(1) 
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)
                
        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

        self.assertEquals("Stopped",elevatorControllerStatusView.cabinStateFieldModel())
        self.assertEquals("Opening",elevatorControllerStatusView.cabinDoorStateFieldModel())
    
if __name__ == "__main__":
    unittest.main()


