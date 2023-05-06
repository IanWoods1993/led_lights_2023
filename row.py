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

def illuminateRow(illuminatedRowNum, r, g, b):
    for i in range(0, numPixels):
        lightIndex = i
        currentColNum = lightIndex // numRows
        isOddCol = currentColNum != 0 and ((currentColNum) % 2) == 1
        if isOddCol and zigZagMode == 1:
            maxColIndex = currentColNum * numRows + 7
            if lightIndex % numRows == illuminatedRowNum:
                pixels[maxColIndex - illuminatedRowNum] = (r, g, b)

        elif lightIndex % numRows == illuminatedRowNum:
            pixels[lightIndex] = (r, g, b)

    pixels.show()

def illuminateRowPositions(illuminatedRowNum):
    positions = []
    for i in range(0, numPixels):
        lightIndex = i
        currentColNum = lightIndex // numRows
        isOddCol = currentColNum != 0 and ((currentColNum) % 2) == 1
        if isOddCol and zigZagMode == 1:
            maxColIndex = currentColNum * numRows + 7
            if lightIndex % numRows == illuminatedRowNum:
                pixels[maxColIndex - illuminatedRowNum] = (r, g, b)

        elif lightIndex % numRows == illuminatedRowNum:
            pixels[lightIndex] = (r, g, b)

    pixels.show()

def main():
    while True:
        pixels.fill((0, 0, 0))
        time.sleep(1)
        illuminateRow(0, 255, 0, 0)
        time.sleep(1)
        illuminateRow(1, 0, 255, 0)
        time.sleep(1)
        illuminateRow(2, 0, 0, 255)
        time.sleep(1)
        illuminateRow(3, 255, 255, 0)
        time.sleep(1)
        illuminateRow(4, 0, 255, 255)
        time.sleep(1)
        illuminateRow(5, 255, 0, 255)
        time.sleep(1)
        illuminateRow(6, 255, 255, 255)
        time.sleep(1)
        illuminateRow(7, 128, 128, 255)
        time.sleep(1)


main()
