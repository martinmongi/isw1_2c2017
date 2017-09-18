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
from abc import ABCMeta, abstractmethod

class Node:
    __metaclass__ = ABCMeta
    STACK_EMPTY_DESCRIPTION = 'Stack is empty'

    @abstractmethod
    def __init__(self, anObject):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

class EmptyNode(Node):
    def __init__(self, anObject):
        self.internal_size = 0
        pass

    def isEmpty(self):
        return True
    
    def value(self):
        raise Exception(self.STACK_EMPTY_DESCRIPTION)

    def size(self):
        return self.internal_size

class NonEmptyNode(Node):
    def __init__(self, anObject, next):
        self.internal_value = anObject
        self.next = next
        self.internal_size = next.internal_size + 1
    
    def isEmpty(self):
        return False
    
    def value(self):
        return self.internal_value
    
    def size(self):
        return self.internal_size

class Stack:

    STACK_EMPTY_DESCRIPTION = 'Stack is empty'

    def __init__(self):
        self.internal_stack = EmptyNode(None)

    def push(self, anObject):
        new_node = NonEmptyNode(anObject, self.internal_stack)
        self.internal_stack = new_node
    
    def pop(self):
        aux = self.internal_stack.value()
        self.internal_stack = self.internal_stack.next
        return aux
    
    def top(self):
        return self.internal_stack.value()
    
    def isEmpty(self):
        return self.internal_stack.isEmpty()
    
    def size(self):
        return self.internal_stack.size()
    
class StackTest(unittest.TestCase):
    
    def testStackShouldBeEmptyWhenCreated(self):
        stack = Stack()
        
        self.assertTrue(stack.isEmpty())

    def testPushAddElementsToTheStack(self):
        stack = Stack()
        stack.push('something')
        
        self.assertFalse(stack.isEmpty())

    def testPopRemovesElementsFromTheStack(self):
        stack = Stack()
        stack.push("Something")
        stack.pop()
        
        self.assertTrue(stack.isEmpty())
    
    def testPopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"
        stack.push(pushedObject)
        self.assertEquals(pushedObject, stack.pop())
    
    def testStackBehavesLIFO(self):
        firstPushed = "First"
        secondPushed = "Second"
        stack = Stack()
        stack.push(firstPushed)
        stack.push(secondPushed)
        
        self.assertEquals(secondPushed,stack.pop())
        self.assertEquals(firstPushed,stack.pop())
        self.assertTrue(stack.isEmpty())
    
    def testTopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals(pushedObject, stack.top())

    def testTopDoesNotRemoveObjectFromStack(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals( 1,stack.size()) 
        stack.top()
        self.assertEquals( 1,stack.size())

    def testCanNotPopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()
        
        try:
            stack.pop()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)
        
    def testCanNotTopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()

        try:
            stack.top()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)
    
if __name__ == "__main__":
    unittest.main()
