import random
canvasSize = (1500, 800)

heuristics = ["FFIT", "BFIT", "WFIT", "AWFIT"]

# SAMPLE INSTANCE
# INSTANCE 392 - HardWF 20
# EXPERIMENT 1
"""solutionsList = [ \
                 ['AWFIT', 'FFIT', 'AWFIT', 'AWFIT', 'WFIT', 'FFIT', 'WFIT', 'WFIT', 'BFIT', 'FFIT', 'BFIT', 'FFIT', 'WFIT', 'FFIT', 'AWFIT', 'FFIT', 'FFIT', 'FFIT', 'FFIT', 'WFIT'], \
                 ['FFIT', 'FFIT', 'FFIT', 'AWFIT', 'FFIT', 'FFIT', 'BFIT', 'BFIT', 'BFIT', 'AWFIT', 'BFIT', 'AWFIT', 'FFIT', 'FFIT', 'BFIT', 'FFIT', 'FFIT', 'FFIT', 'WFIT', 'FFIT'], \
                 ['WFIT', 'BFIT', 'WFIT', 'FFIT', 'FFIT', 'BFIT', 'FFIT', 'WFIT', 'WFIT', 'WFIT', 'BFIT', 'FFIT', 'BFIT', 'WFIT', 'FFIT', 'AWFIT', 'AWFIT', 'WFIT', 'WFIT', 'AWFIT'], \
                 ['FFIT', 'FFIT', 'BFIT', 'BFIT', 'BFIT', 'FFIT', 'FFIT', 'BFIT', 'AWFIT', 'FFIT', 'BFIT', 'FFIT', 'AWFIT', 'FFIT', 'FFIT', 'WFIT', 'WFIT', 'WFIT', 'BFIT', 'FFIT'] \
                 ]
# EXPERIMENT 2
solutionsList.extend([ \
                      ['WFIT', 'AWFIT', 'WFIT', 'FFIT', 'WFIT', 'BFIT', 'BFIT', 'WFIT', 'BFIT', 'AWFIT', 'FFIT', 'AWFIT', 'BFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'WFIT', 'BFIT', 'WFIT'], \
                      ['BFIT', 'WFIT', 'AWFIT', 'BFIT', 'AWFIT', 'FFIT', 'FFIT', 'FFIT', 'WFIT', 'WFIT', 'BFIT', 'AWFIT', 'BFIT', 'BFIT', 'FFIT', 'BFIT', 'BFIT', 'AWFIT', 'FFIT', 'BFIT'], \
                      ['AWFIT', 'WFIT', 'FFIT', 'BFIT', 'FFIT', 'WFIT', 'AWFIT', 'FFIT', 'WFIT', 'FFIT', 'BFIT', 'AWFIT', 'BFIT', 'AWFIT', 'WFIT', 'AWFIT', 'AWFIT', 'FFIT', 'AWFIT', 'WFIT'] \
                      ])
"""
# SAMPLE INSTANCE
# INSTANCE 376 - HardWF 40
solutionsList = [\
                 ['AWFIT', 'WFIT', 'BFIT', 'AWFIT', 'WFIT', 'WFIT', 'AWFIT', 'AWFIT', 'FFIT', 'BFIT', 'BFIT', 'WFIT', 'FFIT', 'WFIT', 'AWFIT', 'FFIT', 'FFIT', 'AWFIT', 'AWFIT', 'BFIT', 'BFIT', 'AWFIT', 'BFIT', 'AWFIT', 'BFIT', 'AWFIT', 'AWFIT', 'WFIT', 'AWFIT', 'BFIT', 'FFIT', 'FFIT', 'WFIT', 'BFIT', 'AWFIT', 'BFIT', 'WFIT', 'BFIT', 'AWFIT', 'AWFIT'], \
                 ['WFIT', 'AWFIT', 'AWFIT', 'WFIT', 'FFIT', 'AWFIT', 'BFIT', 'BFIT', 'BFIT', 'FFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'BFIT', 'WFIT', 'FFIT', 'BFIT', 'AWFIT', 'FFIT', 'BFIT', 'FFIT', 'AWFIT', 'BFIT', 'WFIT', 'WFIT', 'WFIT', 'AWFIT', 'WFIT', 'AWFIT', 'FFIT', 'AWFIT', 'FFIT', 'FFIT', 'AWFIT', 'BFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'BFIT'] \
                 ]

# EXPERIMENT 2
solutionsList.extend([['WFIT', 'WFIT', 'WFIT', 'BFIT', 'WFIT', 'WFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'FFIT', 'BFIT', 'FFIT', 'FFIT', 'FFIT', 'BFIT', 'FFIT', 'WFIT', 'FFIT', 'FFIT', 'BFIT', 'AWFIT', 'FFIT', 'BFIT', 'BFIT', 'BFIT', 'BFIT', 'WFIT', 'WFIT', 'AWFIT', 'AWFIT', 'WFIT', 'BFIT', 'BFIT', 'AWFIT', 'FFIT', 'AWFIT', 'AWFIT', 'AWFIT']])

# EXPERIMENT 3
solutionsList.extend([ \
                      ['AWFIT', 'WFIT', 'WFIT', 'FFIT', 'AWFIT', 'WFIT', 'AWFIT', 'AWFIT', 'WFIT', 'BFIT', 'AWFIT', 'WFIT', 'BFIT', 'WFIT', 'BFIT', 'BFIT', 'FFIT', 'AWFIT', 'WFIT', 'FFIT', 'AWFIT', 'AWFIT', 'FFIT', 'AWFIT', 'AWFIT', 'BFIT', 'BFIT', 'FFIT', 'WFIT', 'AWFIT', 'FFIT', 'FFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'AWFIT', 'FFIT', 'FFIT', 'AWFIT'], \
                      ['AWFIT', 'WFIT', 'WFIT', 'FFIT', 'AWFIT', 'WFIT', 'AWFIT', 'AWFIT', 'WFIT', 'BFIT', 'AWFIT', 'WFIT', 'BFIT', 'WFIT', 'BFIT', 'BFIT', 'FFIT', 'AWFIT', 'WFIT', 'FFIT', 'AWFIT', 'AWFIT', 'FFIT', 'AWFIT', 'AWFIT', 'FFIT', 'FFIT', 'BFIT', 'WFIT', 'WFIT', 'FFIT', 'FFIT', 'AWFIT', 'AWFIT', 'WFIT', 'AWFIT', 'BFIT', 'AWFIT', 'BFIT', 'AWFIT'] \
                      ])


# Variable that controls the display
visualToShow = "GROUP-TREE"

# Variables required to draw the tree
yCoord = 10
xCoords = []
step = 100
spacing = 1000
spaceRatio = 5
prevSelCoords = [None, None]
centroid = []
solutionColors = [(25*random.randint(0,10), 25*random.randint(0,10), 25*random.randint(0,10), 200) for _ in solutionsList]

nDia = 30 # Diameter of the nodes
nRad = nDia / 2 # Radius of the nodes

# Variables required for zooming and paning
zoomScale = 1
xPan = -canvasSize[0] / 2
yPan = -canvasSize[1] / 2
zoomIn = False
zoomOut = False
panUp = False
panDown = False
panLeft = False
panRight = False
panSpeed = 50
zoomSpeed = 1.04

# Function to adjust the X coordinates of the nodes to pretty print them
def adjustCoordsX(coordsList, centroidList, switch = False):
    if switch:
        adjustedCoords = list(coordsList)
            
        orderedCentroid = [centroidList.index(c) for c in centroidList]
        print(orderedCentroid[:-1])
        
        for i in orderedCentroid[:-1]:
            if max(coordsList[i]) > min(coordsList[i]):
                adjustedCoords[i] = [coord-100 for coord in adjustedCoords[i]]
        
        
        return adjustedCoords
    else:
        return coordsList

# Function to detect mouse position
def isMouseOver(x, y, w, h):
    if(mouseX >= x and mouseX <= x+w and mouseY >= y and mouseY <= y+h):
        return True
    return False


def setup():
    size(*canvasSize)

def draw():
    global yCoord, xCoords, solutionsList, prevSelCoords, centroid, zoomScale, xPan, yPan, zoomIn, zoomOut, \
    panUp, panDown, panLeft, panRight, panSpeed, zoomSpeed, adjustCoordsX, visualToShow, spacing, spaceRatio
    
    background(255,255,255)
    fill(0,0,0)
    # Button to Display the tree
    rect(20, 20, 150, 50)
    rect(20, 90, 150, 50)
    rect(20, 160, 150, 50)
    
    fill(0,0,0) if(isMouseOver(20, 20, 150, 50)) else fill(255,255,255)
    rect(25, 25, 140, 40)
    textSize(32)
    fill(255,255,255) if(isMouseOver(20, 20, 150, 50)) else fill(0,0,0)
    text("H. Space", 30, 60)
    
    fill(0,0,0) if(isMouseOver(20, 90, 150, 50)) else fill(255,255,255)
    rect(25, 95, 140, 40)
    textSize(32)
    fill(255,255,255) if(isMouseOver(20, 90, 150, 50)) else fill(0,0,0)
    text("I. Trees", 30, 130)
    
    fill(0,0,0) if(isMouseOver(20, 160, 150, 50)) else fill(255,255,255)
    rect(25, 165, 140, 40)
    textSize(32)
    fill(255,255,255) if(isMouseOver(20, 160, 150, 50)) else fill(0,0,0)
    text("Swimlane", 30, 200)
    
    translate(width/2, height/2)
    scale(zoomScale)
    translate(xPan, yPan)
    
    if(visualToShow == "GROUP-TREE"):
        yCoord = 10
        spacing = 30
        strokeWeight(2)
        for heuristicNum in range(-1, len(solutionsList[0])):
            # Initial node (no selection yet)
            if heuristicNum == -1:
                fill(0, 0, 0)
                ellipse(width / 2, yCoord, nDia, nDia)
                noFill()
                prevSelCoords = [[width / 2, yCoord] for _ in solutionsList]
                centroid = [(width / 2) for _ in solutionsList]
            else:
                xCoords = [[centroid[solutionNum] - (spacing * 3), \
                            centroid[solutionNum] - (spacing * 1), \
                            centroid[solutionNum] + (spacing * 1), \
                            centroid[solutionNum] + (spacing * 3)] for solutionNum in range(len(solutionsList))]
                
                xCoords = adjustCoordsX(xCoords, centroid)
                
                for solutionNum in range(len(solutionsList)):
                    xSelect = xCoords[solutionNum].pop(heuristics.index(solutionsList[solutionNum][heuristicNum]))
                    centroid[solutionNum] = xSelect
                    
                    fill(*solutionColors[solutionNum])
                        
                    ellipse(xSelect, yCoord, nDia, nDia)
                    noFill()
                    ellipse(xCoords[solutionNum][0], yCoord, nDia, nDia)
                    ellipse(xCoords[solutionNum][1], yCoord, nDia, nDia)
                    ellipse(xCoords[solutionNum][2], yCoord, nDia, nDia)
                    
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xSelect, yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][0], yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][1], yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][2], yCoord-nRad)
                    
                    prevSelCoords[solutionNum][0] = xSelect
                    prevSelCoords[solutionNum][1] = yCoord
                    
                #spacing -= spaceRatio
                
            yCoord += step
        
        yCoord = 10
        prevSelCoords = (width / 2, yCoord)
        centroid = width / 2
        strokeWeight(1)
    
    elif(visualToShow == "INDIVIDUAL-TREE"):
        spacing = 20
        strokeWeight(2)
        for heuristicNum in range(-1, len(solutionsList[0])):
            # Initial node (no selection yet)
            if heuristicNum == -1:
                centroid = [solNum*750 for solNum in range(len(solutionsList))]
                prevSelCoords = [[c, yCoord] for c in centroid]
                rootNodeCoords = list(prevSelCoords)
            else:
                xCoords = [[centroid[solutionNum] - (spacing * 3), \
                            centroid[solutionNum] - (spacing * 1), \
                            centroid[solutionNum] + (spacing * 1), \
                            centroid[solutionNum] + (spacing * 3)] for solutionNum in range(len(solutionsList))]
                
                xCoords = adjustCoordsX(xCoords, centroid)
                
                for solutionNum in range(len(solutionsList)):
                    noFill()
                    ellipse(rootNodeCoords[solutionNum][0], rootNodeCoords[solutionNum][1], nDia, nDia)
                
                    xSelect = xCoords[solutionNum].pop(heuristics.index(solutionsList[solutionNum][heuristicNum]))
                    centroid[solutionNum] = xSelect
                    
                    fill(*solutionColors[solutionNum])
                        
                    ellipse(xSelect, yCoord, nDia, nDia)
                    noFill()
                    ellipse(xCoords[solutionNum][0], yCoord, nDia, nDia)
                    ellipse(xCoords[solutionNum][1], yCoord, nDia, nDia)
                    ellipse(xCoords[solutionNum][2], yCoord, nDia, nDia)
                    
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xSelect, yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][0], yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][1], yCoord-nRad)
                    line(prevSelCoords[solutionNum][0], prevSelCoords[solutionNum][1]+nRad, xCoords[solutionNum][2], yCoord-nRad)
                    
                    prevSelCoords[solutionNum][0] = xSelect
                    prevSelCoords[solutionNum][1] = yCoord
                
            yCoord += 60
        
        yCoord = 10
        prevSelCoords = (width / 2, yCoord)
        centroid = width / 2
        strokeWeight(1)
        
    elif(visualToShow == "HEATMAP-SWIMLANE"):
        
        heuristicCount = [[0 for _ in solutionsList[0]] for _ in heuristics]
        
        # Fill the grid
        for solutionNum in range(len(solutionsList)):
            for x in range(len(solutionsList[solutionNum])):
                y = heuristics.index(solutionsList[solutionNum][x])
                heuristicCount[y][x] += 1
                noStroke()
                fill(255, 0, 0, 75)
                rect((width/4) + (x*40), (height/2) + (y*40), 40, 40)
        stroke(0,0,0)
        
        # Draw the grid of the swimlane
        for x in range(len(solutionsList[0])):
            for y in range(len(heuristics)):
                noFill()
                strokeWeight(2)
                rect((width/4) + (x*40), (height/2) + (y*40), 40, 40)
                strokeWeight(1)
                
        # Display the labels
        for x in range(len(solutionsList[0])):
            for y in range(len(heuristics)):
                fill(0,0,0)
                text(heuristics[y], (width/4) - 100, (height/2) + (y*40) + 30)
                text(x+1, (width/4) + (x*40) + 5, (height/2)-10)
                textSize(20)
                text(heuristicCount[y][x], (width/4) + (x*40) + 5, (height/2) + (y*40)+30)
                textSize(32)
                
        
    if(zoomIn):
        zoomScale *= zoomSpeed
    if(zoomOut):
        zoomScale /= zoomSpeed
    if(panUp):
        yPan += panSpeed
    if(panDown):
        yPan -= panSpeed
    if(panLeft):
        xPan += panSpeed
    if(panRight):
        xPan -= panSpeed

# Functions to detect keystrokes and mouse input
def mousePressed():
    global visualToShow
    
    if(isMouseOver(20, 20, 150, 50)):
        visualToShow = "GROUP-TREE"
    if(isMouseOver(20, 90, 150, 50)):
        visualToShow = "INDIVIDUAL-TREE"
    if(isMouseOver(20, 160, 150, 50)):
        visualToShow = "HEATMAP-SWIMLANE"

def keyPressed():
    global zoomIn, zoomOut, panUp, panDown, panLeft, panRight
    if(keyCode == UP):
        zoomIn = True
        zoomOut = False
    if(keyCode == DOWN):
        zoomOut = True
        zoomIn = False
    if(key == "w"):
        panUp = True
        panDown = False
    if(key == "s"):
        panDown = True
        panUp = False
    if(key == "a"):
        panLeft = True
        panRight = False
    if(key == "d"):
        panRight = True
        panLeft = False
        
def keyReleased():
    global zoomIn, zoomOut, panUp, panDown, panLeft, panRight
    if(keyCode == UP):
        zoomIn = False
    if(keyCode == DOWN):
        zoomOut = False
    if(key == "w"):
        panUp = False
    if(key == "s"):
        panDown = False
    if(key == "a"):
        panLeft = False
    if(key == "d"):
        panRight = False
