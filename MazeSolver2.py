import cv2
from stack_array import *


class Node:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return "Row: " + str(self.row) +  "  Col: " + str(self.col)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

class NodeGraph:

    def __init__(self, image):

        self.imageIn = cv2.imread(image)
        self.rows, self.columns, self.channels = self.imageIn.shape
        self.adjacency = {}
        self.visited = {}
        self.path = []

        self.parse()

        self.solveMaze()
        print(self.path)
        self.drawSolution()


    def parse(self):

        image = self.imageIn

        for col in range(5, self.columns, 10):
            for row in range(5, self.rows, 10):
                wallCheck = [Node(row + 5, col), Node(row, col + 5), Node(row -5, col), Node(row, col -5)]
                possibleAdj = [Node(row + 10, col), Node(row, col + 10), Node(row - 10, col), Node(row, col - 10)]
                actualAdj = []
                current = Node(row, col)

                for i in range(len(possibleAdj)):
                    if self.validNode(wallCheck[i]) and self.validNode(possibleAdj[i]):
                        actualAdj.append(possibleAdj[i])
                        self.visited[possibleAdj[i]] = False

                self.adjacency[current] = actualAdj

    def validNode(self, node):
        return 0 < node.row < self.rows and 0 < node.col < self.columns \
               and not str(self.imageIn[node.row, node.col]) == "[0 0 0]"


    def solveMaze(self):

        stack = Stack(self.rows * self.columns)
        previous = {}
        start = Node(5, 5)

        stack.push(start)
        previous[start] = None

        while not stack.is_empty():
            current = stack.pop()
            self.visited[current] = True

            if current.row == self.rows - 5 and current.col == self.columns - 5:
                self.path.append(current)
                while previous[current] is not None:
                    self.path.append(previous[current])
                    current = previous[current]
                return

            for node in self.adjacency[current]:
                if not self.visited[node]:
                    previous[node] = current
                    self.visited[node] = True
                    stack.push(node)

    def drawSolution(self):
        im = self.imageIn
        for node in self.path:
            row, col = node.row, node.col
            im = cv2.rectangle(im, (col - 2, row-2), (col + 2, row + 2), (128, 0, 0), -1)
        cv2.imwrite("MazeSolve.png", im)



NodeGraph("Maze.png")