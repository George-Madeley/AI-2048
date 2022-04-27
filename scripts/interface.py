"""
This script holds the functionality for the program to take a screenshot, read data from the screen shot and enter in controls.
"""

import math
import pyautogui
from PIL import Image
from pynput.keyboard import Key, Controller


def DivideImage(image: Image, config: dict) -> list:
    """
    Divides up the provided image of 2048 intol 16 smaller images
    
    Args:
        image: The image of 2048.
        config: The dictionary of configuration values.

    Returns:
        2D-list of Images.
    """
    dividedImage = []
    gridSize = config["2048"]["gridsize"]
    # The Width between each numbers box
    width = math.floor(config["2048"]["size"]["x"] / gridSize)
    # the hieght between each numbers box
    height = math.floor(config["2048"]["size"]["y"] / gridSize)
    # The size of the color sample area
    sampleBox = config["2048"]["box"]["x"]
    for y in range(gridSize):
        dividedRow = []
        for x in range(gridSize):
            # left, upper, right, lower bounds
            tempBoxSize = (x * width, y * height, x * width + sampleBox, y * width + sampleBox)
            tempImage = image.crop(box=tempBoxSize)
            # tempImage.show()
            dividedRow.append(tempImage)
        dividedImage.append(dividedRow)
    return dividedImage

def GetTileNumber(image: Image, colorConfig: dict) -> int:
    """
    Gets the background color of the image.

    Args:
        image: The image to find the color in.

    Returns:
        The number in the tile.
    """
    color = GetColorValue(image)
    for number, colorCode in colorConfig.items():
        if (colorCode["r"] == color["r"] and
            colorCode["g"] == color["g"] and
            colorCode["b"] == color["b"]):
            return number
    return None

def GetColorValue(image: Image) -> dict:
    """
    Gets the average RGB values for the past in image.
    
    Args:
        image: The image to get the RGB values from.
        
    Returns:
        A dict of the R,G,B values.
    """

    # image.show()
    colors = image.getcolors()
    #colors = [color for color in colors if (color[-1][0] < upperWeight or color[-1][1] < upperWeight or color[-1][2] < upperWeight)]
    finalColor = [0, 0, 0]
    for color in colors:
        finalColor[0] += color[-1][0]
        finalColor[1] += color[-1][1]
        finalColor[2] += color[-1][2]
    finalColor[0] /= len(colors)
    finalColor[1] /= len(colors)
    finalColor[2] /= len(colors)
    return {
        "r": finalColor[0],
        "g": finalColor[1],
        "b": finalColor[2]
    }

def GetInformation(config: dict, colorConfig: dict):
    """
    Reads the screen to update the programs copy of the current state of 2048.
    
    Args:
        config: (dict) The config of the app.
        colorConfig: (dict) The config of the colors.

    Returns:
        A 2D-list of a integer representation of the current game state.
    """

    filePath = GetScreenshot()
    with Image.open(filePath) as screenshot:
        # left, upper, right, lower bounds
        upperX = config["2048"]["pos"]["x"]
        upperY = config["2048"]["pos"]["y"]
        lowerX = upperX + config["2048"]["size"]["x"]
        lowerY = upperY + config["2048"]["size"]["y"]
        cropBoxSize = (upperX, upperY, lowerX, lowerY)
        image = screenshot.crop(box=cropBoxSize)
        # wordleImage.show()

        dividedImage = DivideImage(image, config)
        tileNumberList = [[GetTileNumber(sampleImage) for sampleImage in dividedImage[row]] for row in range(len(dividedImage))]
        return tileNumberList
    
def GetScreenshot() -> str:
    """
    Takes a screenshot and returns the file path to the screenshot.
    
    Returns:
        The string of the screenshot filepath.
    """

    pyautogui.screenshot('images\shot.png')
    return 'images\shot.png'

def PressKey(keyNum: int) -> None:
    """
    Enters up, down, left, or right on to the game.

    Args:
        keyNum: integer representing the key to be pressed.
            0 - Up,
            1 - Right,
            2 - Down,
            3 - Left
    """

    keyboard = Controller()
    if keyNum == 0:
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif keyNum == 1:
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif keyNum == 2:
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif keyNum == 3:
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    else:
        raise ValueError
        