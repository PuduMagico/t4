import random
import operator
import sys
sys.setrecursionlimit(20000)

class Node(object):
    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val
        self.childrenAreTerminal = None
        self.children = None
        self.isLeaf = False

    def generateTree(self,  height, terminals, operations):
        rand = random.randint(0,1)
        if not self.isLeaf:
            if height == 0:
                self.left = Node(random.choice(terminals))
                self.left.printTree
                self.left.isLeaf = True
                self.right = Node(random.choice(terminals))
                self.right.printTree

                self.right.isLeaf = True
                self.right.printTree

            else:
                if rand > 0.5:
                    self.left = Node(random.choice(operations))
                else:
                    self.left = Node(random.choice(terminals))
                    self.left.isLeaf = True
                if rand > 0.5:
                    self.right = Node(random.choice(operations))
                else:
                    self.right = Node(random.choice(terminals))
                    self.right.isLeaf = True

                self.left.generateTree(height - 1, terminals, operations)
                self.right.generateTree(height - 1, terminals, operations)

    def setLeftChild(self, child):
        self.left = child

    def setRightChild(self, child):
        self.right = child

    def printTree(self, level = 0):
        print '\t' * level + str(self.value)
        if self.isLeaf:
            pass
        else:
            self.left.printTree(level + 1)
            self.right.printTree(level + 1)

    def evaluate(self):
        if not self.isLeaf:
            left = self.left.evaluate()
            right = self.right.evaluate()
            if self.value == '+':
                return left + right
            elif self.value == '*':
                return left * right
            elif self.value == '-':
                return left - right
            else:
                # Protective Division
                if right == 0:
                    return 1
                else:
                    return left/right
        else:
            return self.value

    def randomNode(self):
        if random.randint(0,1) > 0.9:
            return self
        else:
            if not self.isLeaf:
                if random.randint(0,1) > 0.5:
                    return self.left.randomNode()
                else:
                    return self.right.randomNode()

    # def crossOver(self, subtree):
    #     # if random.randint(0,1) > 0.5:
    #     #     self = subtree
    #     # else:
    #     if not self.isLeaf:
    #         if random.randint(0,1) > 0.5:
    #             if self.left.isLeaf:
    #                 self.left = subtree
    #             else:
    #                 self.left.crossOver(subtree)
    #         else:
    #             if self.right.isLeaf:
    #                 self.right = subtree
    #             else:
    #                 self.right.crossOver(subtree)

    def mutate(self, mutProb, terminals, operations):
        rand = random.randint(0,1)
        if self.isLeaf:
            if rand > mutProb:
                self.value = random.choice(terminals)
        else:
            if rand > mutProb:
                self.value = random.choice(operations)
            self.left.mutate(mutProb, terminals, operations)
            self.right.mutate(mutProb, terminals, operations)


class Tree(object):
    def __init__(self, terminals):
        self.height = 1
        self.operations = ['+', '-', '*', '/']
        if terminals == "numbers":
            self.terminals = list(range(0,10))
        else:
            self.terminals = list(map(chr, range(97, 123)))
        self.root = Node(random.choice(self.operations))

        self.crossOvered = False



    def randomNode(self):
        return self.root.randomNode()

    def crossOver(self, subtree):
        done = False
        ancestor = self.root
        while not done:
            if not ancestor.isLeaf:
                if random.randint(0,1) > 0.5:
                    if random.randint(0,1) > 0.8:
                        ancestor.left = subtree
                        done = True
                    else:
                        ancestor = ancestor.left
                else:
                    if random.randint(0,1) > 0.8:
                        ancestor.right = subtree
                        done = True
                    else:
                        ancestor = ancestor.right
            else:
                ancestor = self.root
            # self.root.crossOver(subtree)

    def getHeight(self):
        return self.height

    def getRoot(self):
        return self.root

    def grow(self, height):
        self.root.generateTree(height, self.terminals, self.operations)

    def printTree(self):
        self.root.printTree()

    def evaluate(self):
        return self.root.evaluate()

    def mutate(self, mutationProb):
        self.root.mutate(mutationProb, self.terminals, self.operations)

class GP(object):
    def __init__(self, populationSize, generations, crossOverProb, mutationProb, maxHeight):
        self.populationSize = populationSize
        self.population = []
        self.matingPool = []
        self.fittest = []
        self.generations = generations
        self.crossOverProb = crossOverProb
        self.mutationProb = mutationProb
        self.maxHeight = maxHeight

    def generateInitialPopulation(self):
        for i in range(self.populationSize):
            newTree = Tree("numbers")
            newTree.grow(random.randint(1,self.maxHeight))
            self.population.append(newTree)

    def testAndSelectFittest(self, goal):
        fitMeasure = []
        for tree in self.population:
            answer = tree.evaluate()
            print(answer)
            fitness = goal - answer
            print(fitness)
            if fitness == 0:
                print("Encontramos un ganador!")
                return tree
            fitMeasure.append((tree,answer))
        fitMeasure.sort(key=operator.itemgetter(1), reverse = True)
        fittest = fitMeasure[0:len(fitMeasure)/2]
        self.fittest = [x[0] for x in fittest]

    def loveTime(self):
        self.population = []

        for tree in self.fittest:
            self.population.append(tree)

        for i in range(self.populationSize - len(self.population)):
            papa, mama = random.sample(self.fittest,2)

            crossOverPoint = None
            while crossOverPoint == None:
                crossOverPoint = papa.randomNode()
            hijo = Tree("numbers")
            mama.crossOver(crossOverPoint)
            hijo.root = mama.root

            hijo = mama
            self.population.append(hijo)

    def mutate(self):
        for tree in self.population:
            tree.mutate(self.mutationProb)

    def showTrees(self):
        for tree in self.population:
            tree.printTree()


if __name__ == "__main__":
    GP = GP(8, 100, 0.9, 0.1, 6)
    GP.generateInitialPopulation()
    flag = True
    generacion = 0
    while flag:
        print("generacion")
        print(generacion)
        generacion += 1
        x = GP.testAndSelectFittest(500)
        if x != None:
            flag = False
            print("Terminamos")
        GP.loveTime()
        # GP.mutate()
