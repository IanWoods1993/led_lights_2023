# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random
import getch
import sys
import select
import tty
import termios

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

numRows = 8
numColumns = 5
# 0 for no zigzag, 1 for zigzag
zigZagMode = 1

# The number of NeoPixels
numPixels = numRows * numColumns

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, numPixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

userInput = ""
illuminatedPositions = []
x = 0
y = 0
applePos = ()
tailLen = 1
lastCommand = "w"

def illuminatePosition2d(x, y, r, g, b):
    position = x * numRows + y
    positionColNum = position // numRows
    isOddCol = positionColNum != 0 and ((positionColNum) % 2) == 1
    print("About to illuminate coordinates (x, y): (" + str(x) + ", " + str(y) + ") for position " + str(position))
    if isOddCol and zigZagMode == 1:
        maxColIndex = positionColNum * numRows + numRows - 1
        pixels[maxColIndex - y] = (r, g, b)
    else:
        pixels[position] = (r, g, b)
    
    pixels.show()


def flashColorFor(r, g, b, durationSeconds):
    i = 0
    while i < durationSeconds:
        pixels.fill((r, g, b))
        pixels.show()
        time.sleep(0.5)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)
        i = i + 1

def init():
    global x
    global y
    global illuminatedPositions
    pixels.fill((0, 0, 0))
    pixels.show()
    illuminatedPositions.clear()
    x = 0
    y = 0
    illuminatePosition2d(x, y, 0, 0, 255)
    illuminatedPositions.append((x, y))
    createApple()

def createApple():
    global illuminatedPositions
    global applePos
    applePlaced = False
    while not applePlaced:
        randX = random.randint(0, numColumns - 1)
        randY = random.randint(0, numRows - 1)
        print("x: " + str(randX) + ", y: " + str(randY))
        if (randX, randY) in illuminatedPositions:
            continue
        else:
            applePos = (randX, randY)
            illuminatePosition2d(randX, randY, 0, 255, 0)
            return

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getPositionDelta():
    global lastCommand
    userInput = lastCommand

    if isData():
        userInput = sys.stdin.read(1)

    pos = [0, 0]
    if userInput == "w":
        pos[1] = 1
    elif userInput == "a":
        pos[0] = -1
    elif userInput == "s":
        pos[1] = -1
    elif userInput == "d":
        pos[0] = 1

    lastCommand = userInput
    return pos

def main():
    init()
    global x
    global y
    global illuminatedPositions
    global applePos
    global tailLen
    old_settings = termios.tcgetattr(sys.stdin)
    sleepTime = 1
    try:
        tty.setcbreak(sys.stdin.fileno())

        while True:
            foundApple = False
            delta = getPositionDelta()
            x = x + delta[0]
            y = y + delta[1]
            if x == numColumns:
                x = 0
            elif x == -1:
                x = numColumns - 1

            if y == numRows:
                y = 0
            elif y == -1:
                y = numRows - 1

            illuminatePosition2d(x, y, 0, 0, 255)
            positionTuple = (x, y)
            if positionTuple in illuminatedPositions:
                flashColorFor(255, 0, 0, 4)
                print("You collided with yourself")
                break 
            else:
                illuminatedPositions.append(positionTuple)

            if (x, y) == applePos:
                foundApple = True
                tailLen = tailLen + 1
                createApple()
                if sleepTime > 0.2:
                    sleepTime = sleepTime - .1
            
            
            if not foundApple:
                obsoletePosition = illuminatedPositions.pop(0)
                illuminatePosition2d(obsoletePosition[0], obsoletePosition[1], 0, 0, 0)
            time.sleep(sleepTime)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


main()
