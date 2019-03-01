from random import *
import cv2
import numpy as np


class Cell:

    def __init__(self, x, y):
        self.color = (0, 0, 0)
        self.visited = False
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x < other.x:
            return True

        elif self.x == other.x:
            if self.y < other.y:
                return True

        return False

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def switchColor(self):
        if self.color == (0,0,0):
            self.color = (255,255,255)
            return True

        return False





class Maze:

    def __init__(self, image_insert):
        # self.image = cv2.imread(image_insert, 0)
        self.image = image_insert
        self.pixelwidth, self.pixelheight = self.image.shape[:2]

        self.width = self.pixelwidth // 10
        self.height = self.pixelheight // 10
        self.maze = self.initMaze()
        self.edges = self.initEdges()
        self.initMaze()
        self.drawMaze()


    def initMaze(self):
        maze = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]
        for h in range(self.height):
            for w in range(self.width):
                maze[w][h] = Cell(w, h)  # Initializes empty cells in 2d array

        return maze

    def initEdges(self):
        edges = [[[] for y in range(self.height)] for x in range(self.width)]

        for w in range(self.width):
            for h in range(self.height):
                array = self.findTouching(self.maze[w][h])   # Adds all cells touching one cell to list of edges
                edges[w][h] = array  # Adds adjacent cells as 'edges' to  original cell location in 2d array

        return edges

    def drawMaze(self):
        im = self.image
        for w in range(0, self.pixelwidth, 10):
            for h in range(0, self.pixelheight, 10):
                if self.maze[w // 10][h // 10].color == (255, 255, 255):  # If the square is white, draw it as white
                    ph = h + 2   # This is really a safety mechanism as all squares in theory should be white
                    pw = w + 2
                    im = cv2.rectangle(im, (pw, ph), (w+7, h+7), self.maze[w // 10][h // 10].color, -1)

        cv2.imwrite("Maze.png", im)  # Write image to file
        self.image = cv2.imread("Maze.png", 1)  # Set maze self.image to the file

    def drawconnections(self):
        im = self.image
        for w in range(self.width):
            for h in range(self.height):
                if self.maze[w][h].color == (255,255,255):
                    touching = self.findTouching(self.maze[w][h])  # Identify all cells directly adjacent
                    for cell in touching:
                        if self.maze[cell.x][cell.y] not in self.edges[w][h]:  # If cell is not also a 'edge' draw a connection
                            if cell.y < h:
                                im = cv2.rectangle(im, (w * 10 + 2, cell.y * 10 + 7), (w * 10 + 7, h * 10 +2), (255, 255, 255), -1)

                            if cell.y > h:
                                im = cv2.rectangle(im, (w * 10 + 2, h * 10+ 7), (w * 10 + 7, cell.y * 10 + 2), (255, 255, 255), -1)

                            if cell.x > w:
                                im = cv2.rectangle(im, (w * 10 + 7, h * 10 + 2), (cell.x * 10 + 2, h * 10 + 7), (255, 255, 255), -1)

                            if cell.x < w:
                                im = cv2.rectangle(im, (cell.x * 10 + 7, h * 10 + 2), (w * 10 + 2, h * 10 + 7), (255, 255, 255), -1)

        cv2.imwrite("Maze.png", im)
        self.image = cv2.imread("Maze.png", 1)

    def drawStart(self):
        im = self.image
        im = cv2.rectangle(im, (2, 0), (7, 7), (0, 128, 0), -1)  # Draws green at start
        im = cv2.rectangle(im, (self.pixelwidth - 8, self.pixelheight- 8),
                           (self.pixelwidth - 3, self.pixelheight), (0, 0, 128), -1)  # Draws red at end
        cv2.imwrite("Maze.png", im)
        self.image = cv2.imread("Maze.png", 1)

    def binarySearch(self, alist, item):  # More effective search for cells
        first = 0
        last = len(alist)-1
        found = False
        while first <= last and not found:
            midpoint = (first+last)//2
            if alist[midpoint] == item:
                found = True
            else:
                if item < alist[midpoint]:
                    last = midpoint - 1
                else:
                    first = midpoint + 1
        return found

    def createMazePrim(self):  # This method works the same as randomizedPrim but here the maze is centered around (0,0)
        path = []  # Initialize list of pathsquares

        visited = []  # Initialize list of all visited cells
        self.maze[0][0].switchColor()  # Set the start of the maze to a path color

        walls = []  # Initialize list of walls

        path.append(self.maze[0][0])  # Add the starting block to the path
        startingWalls = [self.maze[0][0]] + self.findTouching(self.maze[0][0])
        walls.append(startingWalls)  # Add the first two walls

        while len(walls) > 0:  # While walls or edges remain

            rando = randint(0, len(walls) - 1)

            randcell = walls[rando]
            rando2 = randint(1, len(randcell) - 1)
            randWall = walls[rando].pop(rando2)  # Choose random cell and get random edge or wall
            appender = [randcell[0]] + [self.maze[randWall.x][randWall.y]]  # appends the visited cell with wall
            visited.append(appender)  # Add wall to visited list

            if not self.maze[randWall.x][randWall.y] in path:  # If the random wall isn't already part of the path

                path.append(self.maze[randWall.x][randWall.y])
                self.maze[randWall.x][randWall.y].switchColor()  # Make the wall a part of the path

                self.edges[randcell[0].x][randcell[0].y].remove(randWall)  # Remove wall from list of 'edges' for...
                # Particular cell. This allows us to draw the connections based on what is not in edges list

                self.edges[randWall.x][randWall.y].remove(randcell[0])   # Vice-versa

                walls.append([randWall] + self.edges[randWall.x][randWall.y])  # Add remaining edges around cell to list

            if len(walls[rando]) == 1:  # If all that's left is identifier cell with no edges, get rid of it from array
                walls.pop(rando)

    def createMazeRandomizedPrim(self):  # This works the same as normal prim but starting point is randomized

        path = []  # Initialize list of pathsquares

        visited = []  # Initialize list of all visited cells
        randomStartW = randint(0, self.width - 1)  # Choose a random starting width
        randomStartH = randint(0, self.height - 1)  # Choose a random starting height
        self.maze[randomStartW][randomStartH].switchColor()  # Set the start of the maze to a path\

        walls = []  # Initialize list of walls

        path.append(self.maze[randomStartW][randomStartH])  # Add the starting block to the path
        startingWalls = [self.maze[randomStartW][randomStartH]] + self.findTouching(self.maze[randomStartW][randomStartH])

        walls.append(startingWalls)  # Add all surrounding walls

        while len(walls) > 0:  # While walls or edges remain

            rando = randint(0, len(walls) - 1)

            randcell = walls[rando]
            rando2 = randint(1, len(randcell) - 1)
            randWall = walls[rando].pop(rando2)  # Choose random cell and get random edge or wall
            appender = [randcell[0]] + [self.maze[randWall.x][randWall.y]]  # appends the visited cell with wall
            visited.append(appender)  # Add wall to visited list

            if not self.maze[randWall.x][randWall.y] in path:  # If the random wall isn't already part of the path

                path.append(self.maze[randWall.x][randWall.y])
                self.maze[randWall.x][randWall.y].switchColor()  # Make the wall a part of the path

                self.edges[randcell[0].x][randcell[0].y].remove(randWall)  # Remove wall from list of 'edges' for...
                # Particular cell. This allows us to draw the connections based on what is not in edges list

                self.edges[randWall.x][randWall.y].remove(randcell[0])   # Vice-versa

                walls.append([randWall] + self.edges[randWall.x][randWall.y])  # Add remaining edges around cell to list

            if len(walls[rando]) == 1:  # If all that's left is identifier cell with no edges, get rid of it from array
                walls.pop(rando)


    def findTouching(self, cell):
        adjacent = []

        w = cell.x
        h = cell.y + 1

        if w >= 0 and h >= 0:
            try:
                adjacent.append(self.maze[w][h])
            except:
                IndexError

        w = cell.x - 1
        h = cell.y

        if w >= 0 and h >= 0:
            try:
                adjacent.append(self.maze[w][h])
            except:
                IndexError

        w = cell.x + 1
        h = cell.y

        if w >= 0 and h >= 0:
            try:
                adjacent.append(self.maze[w][h])
            except:
                IndexError

        w = cell.x
        h = cell.y - 1

        if w >= 0 and h >= 0:
            try:
                adjacent.append(self.maze[w][h])
            except:
                IndexError

        return adjacent


img = np.zeros((1000, 1000, 3), np.uint8)  # Image size in pixels only works with squares

# Takes time past 1000 pixels x 1000 pixels

maze = Maze(img)

# maze.createMazePrim()
maze.createMazeRandomizedPrim()
maze.drawMaze()
maze.drawconnections()
maze.drawStart()

