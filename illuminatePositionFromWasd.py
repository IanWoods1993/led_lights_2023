# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

numRows = 8
numColumns = 4
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

def illuminatePosition2d(x, y, r, g, b):
    position = x * numRows + y
    print("Position to illuminate when x = " + str(x) + " and y = " + str(y) + ": " + str(position))
    positionColNum = position // numRows
    isOddCol = positionColNum != 0 and ((positionColNum) % 2) == 1
    if isOddCol and zigZagMode == 1:
        maxColIndex = positionColNum * numRows + numRows - 1
        pixels[maxColIndex - y] = (r, g, b)
    else:
        pixels[position] = (r, g, b)
    
    pixels.show()

def main():
    illuminatePosition2d(0, 0, 0, 0, 255)
    x = 0
    y = 0
    while True:
        pixels.fill((0, 0, 0))
        userInput = input("Enter wasd: ")
        if userInput == "w":
            y = y + 1
        elif userInput == "a":
            x = x - 1
        elif userInput == "s":
            y = y - 1
        elif userInput == "d":
            x = x + 1
        illuminatePosition2d(x, y, 0, 0, 255)

main()
