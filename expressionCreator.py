import random

class expressionCreator(object):
    def __init__(self):
        self.lastExpression = None
        self.operations = ['+', '-', '*', '/']
        self.numbers = range(0,10)
        self.variables = list(map(chr, range(97, 123)))
    def generateExpression(self, height, terminals):
        for i in range(height):
            if i == height:
                maxchildren = i**2
                children = random(1,maxchildren)
