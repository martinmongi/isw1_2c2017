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

class Stack:

    STACK_EMPTY_DESCRIPTION = 'Stack is empty'

    def __init__(self):
        self.internal_stack = []

    def push(self, anObject):
        self.internal_stack.append(anObject)
    
    def pop(self):
        if len(self.internal_stack) > 0:
            aux = self.internal_stack[-1]
            self.internal_stack.pop()
            return aux
        raise Exception(self.STACK_EMPTY_DESCRIPTION)
    
    def top(self):
        if len(self.internal_stack) > 0:
            return self.internal_stack[-1]
        raise Exception(self.STACK_EMPTY_DESCRIPTION)
    
    def isEmpty(self):
        return len(self.internal_stack) == 0
    
    def size(self):
        return len(self.internal_stack)
    
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
