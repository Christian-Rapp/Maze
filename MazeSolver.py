import cv2
import numpy as np
from stack_array import *

class Node:

    def __init__(self, start=None, connections=[None, None, None, None]):
        self.connections = connections
        if connections[0] is not None:
            self.upl = connections[0].location
        else:
            self.upl = None

        if connections[1] is not None:
            self.downl = connections[1].location
        else:
            self.downl = None

        if connections[2] is not None:
            self.leftl = connections[2].location
        else:
            self.leftl = None

        if connections[3] is not None:
            self.rightl = connections[3].location
        else:
            self.rightl = None
        self.up = connections[0]
        self.down = connections[1]
        self.left = connections[2]
        self.right = connections[3]
        self.visited = False
        self.adjacencylist = []


        self.location = start

    def __repr__(self):

        return str(self.location) + " Up: " + str(self.upl) + " Down: " + str(self.downl) \
               + " Left: " + str(self.leftl) + " Right: " + str(self.rightl)

    def setright(self, node):
        self.right = node
        self.rightl = node

    def setleft(self, node):
        self.left = node
        self.leftl = node

    def setdown(self, node):
        self.down = node
        self.downl = node

    def setup(self, node):
        self.up = node
        self.upl = node

class Graph:

    def __init__(self, startnode, nodelist, endnode):
        self.start = startnode
        self.nodelist = []
        self.end = endnode


class Maze:

    def __init__(self, image):

        self.image = image
        self.mazegraph, self.allnodes, self.pixelwidth, self.pixelheight = self.parsemaze(image)
        self.width = self.pixelwidth // 10
        self.height = self.pixelheight // 10
        # print(self.mazegraph)
        self.connectMazeSucceed()
        self.graph = Graph(self.allnodes[0], self.allnodes, self.allnodes[-1])
        self.solve = self.solveMaze()
        self.drawSolution()

    def parsemaze(self, image):

        image = cv2.imread(image, 1)
        # print(image.shape)
        width, height, channels = image.shape
        allNodes = []
        emptyNodes = []

        for h in range(5, width, 10):
            for w in range(5, height, 10):
                emptyNodes.append(Node((w,h)))
                if not str(image[h, w]) == "[0 0 0]":
                    connections = []
                    try:
                        if not str(image[h-5, w]) == "[0 0 0]":
                            connections.append(Node((w, h - 10)))

                        else:
                            connections.append(None)
                    except:
                        IndexError
                    if not len(connections) == 1:
                        connections.append(None)
                    try:
                        if not str(image[h+5, w]) == "[0 0 0]":
                            connections.append(Node((w, h + 10)))
                        else:
                            connections.append(None)
                    except:
                        IndexError

                    if not len(connections) == 2:
                        connections.append(None)

                    try:
                        if not str(image[h, w-5]) == "[0 0 0]":
                            connections.append(Node((w - 10, h)))
                        else:
                            connections.append(None)
                    except:
                        IndexError

                    if not len(connections) == 3:
                        connections.append(None)

                    try:
                        if not str(image[h, w + 5]) == "[0 0 0]":
                            connections.append(Node((w + 10, h)))
                        else:
                            connections.append(None)
                    except:
                        IndexError

                    if not len(connections) == 4:
                        connections.append(None)

                    # print(connections)
                    point = Node((w, h), connections)
                    allNodes.append(point)
        return allNodes, emptyNodes, width, height

    def connectMazeFAIL(self):

        for i in range(len(self.allnodes)):
            print("FROM MAZEGRAPH", self.mazegraph[i])
            if not self.mazegraph[i].up is None and i > 0:
               self.allnodes[i].setup(self.allnodes[i - self.width])

            if not self.mazegraph[i].down is None and i < len(self.allnodes)-1:
                self.allnodes[i].setdown(self.allnodes[i + self.width])

            if not self.mazegraph[i].left is None:
                self.allnodes[i].setleft(self.allnodes[i - 1])

            if not self.mazegraph[i].right is None:
                self.allnodes[i].setright(self.allnodes[i + 1])



            print("FROM ALL NODES", self.allnodes[i])
            print("______________________________")

    def connectMazeSucceed(self):
        self.allnodes = []
        for node in self.mazegraph:
            adjacency = []
            for direction in node.connections:
                if direction is not None:
                    adjacency.append(direction)
            node.adjacencylist = adjacency
            # print("NODE: ", node, "Adjacent to: ",adjacency)
            self.allnodes.append(node)


    def solveMaze(self):

        notFound = True

        while notFound:

            stack = Stack(self.width * self.height)

            stack.push(self.graph.start)
            currentPath = []
            while not stack.is_empty():

                currentNode = stack.pop()
                # print("current node =", currentNode)
                currentNode.visited = True


                if currentNode is self.graph.end:
                    return currentPath

                unvisitedcount = 0
                for node in currentNode.adjacencylist:

                    if node is not None and not node.visited:
                        unvisitedcount += 1

                if unvisitedcount > 0:
                    for node in currentNode.adjacencylist:

                        if node is not None and not node.visited:
                            currentPath.append(currentNode.location)
                            x ,y = node.location
                            x = (x-5) // 10
                            y = (y -5) // 10
                            if x >= 0 and y >= 0:
                                # print(node.location)
                                stack.push(self.mazegraph[y*self.width + x])
                            node.visited = True
                            self.mazegraph[y * self.width + x].visited = True



    def drawSolution(self):
        im = cv2.imread(self.image, 1)
        for node in self.solve:
            x,y = node
            im = cv2.rectangle(im, (y - 2, x-2), (y + 2, x + 2), (128, 0, 0), -1)
            # im = cv2.rectangle(im, (10, 10), (12, 12), (128,0,0), -1)
        cv2.imwrite("Maze.png", im)
        self.image = cv2.imread("Maze.png", 1)



maze = Maze("Maze.PNG")
print(maze.mazegraph)
print("______________________________")
print(maze.solve)