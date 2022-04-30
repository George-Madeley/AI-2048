"""
Author: George Madeley,
Date: 29/04/2022

Description:
    - Takes screenshots of the game state.
    - Collects information from the screenshot.
    - Translates the data into the correct format.
    - Controls the keyboard.
    - Controls the mouse.
"""

import logging
import math
from statistics import mode
import numpy as np
import pyautogui
from PIL import Image
from streamio import AppendColorFile
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Button, Controller as MouseController


# =======================================
# OUTPUT
# =======================================



def GetInformation(config: dict, colorList: list):
    """
    Reads the screen to update the programs copy of the current state of 2048.
    
    Args:
        config: (dict) The config of the app.
        colorConfig: (dict) The config of the colors.

    Returns:
        A 2D-list of a integer representation of the current game state.
    """

    # Get Screenshot
    filePath = GetScreenshot()
    # Load screenshot
    with Image.open(filePath) as screenshot:
        # Calculate game bounds
        upperX = config["2048"]["pos"]["x"]
        upperY = config["2048"]["pos"]["y"]
        lowerX = upperX + config["2048"]["size"]["x"]
        lowerY = upperY + config["2048"]["size"]["y"]
        cropBoxSize = (upperX, upperY, lowerX, lowerY)
        image = screenshot.crop(box=cropBoxSize)
        # image.show()
        # Divide up image
        dividedImage = DivideImage(image, config)
        # Get list of numbers
        gridsize = config['2048']['gridsize']
        tileNumberList = [[0 for i in range(gridsize)] for j in range(gridsize)]
        tileColorList = [[0 for i in range(gridsize)] for j in range(gridsize)]
        for j in range(gridsize):
            for i in range(gridsize):
                # logging.debug(f'j:{j + 1}, i:{i + 1}')
                sampleImage = dividedImage[j][i]
                tileNumberList[j][i], tileColorList[j][i] = GetTileNumber(
                    sampleImage,
                    colorList,
                    config['knn']
                )
    # logging.debug('If the following correct?')
    # print(np.array(tileNumberList))
    # response = input("Y/N?:\t").lower() == "y"
    # if not response:
    #     print("location?")
    #     x = int(input("X:\t")) - 1
    #     y = int(input("Y:\t")) - 1
    #     sampleImage = dividedImage[y][x]
    #     GetTileNumber(
    #         sampleImage,
    #         colorList,
    #         config['knn'],
    #         record=True,
    #         filepath=config['colors']
    #     )
    return tileNumberList, tileColorList

def GetScreenshot() -> str:
    """
    Takes a screenshot and returns the file path to the screenshot.
    
    Returns:
        The string of the screenshot filepath.
    """

    pyautogui.screenshot('img\shot.png')
    return 'img\shot.png'

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

def CalculateDistance(color1: dict, color2: dict) -> float:
    """
    Calculates the distance between two color values.
    
    Args:
        color1: A dict of rgb color values.
        color2: A dict of rgb color values.
    
    Returns:
        The distance between the two values.
    """

    diffR = color1['r'] - color2['r']
    diffG = color1['g'] - color2['g']
    diffB = color1['b'] - color2['b']
    totalSquared = diffR ** 2 + diffG ** 2 + diffB ** 2
    return float(math.sqrt(totalSquared))

def GetTileNumber(image: Image, colorList: list, K: int  = 3, record: bool = False, filepath: str = None) -> int:
    """
    Gets the background color of the image.

    Args:
        image: The image to find the color in.
        colorConfig: The color configuration dict.
        margin: The color value margin or error.
        filepath: The filepath to the color csv file.

    Returns:
        The number in the tile.
        The np.array of the color values.
    """
    color = GetColorValue(image)
    color = np.array(list(color.values()))
    distances = []
    for number, colorCode in colorList:
        dist = np.linalg.norm(color - colorCode)
        distances.append((number, dist))
    distances.sort(key = lambda x: x[1])
    topK = distances[:K][0]
    top = mode(topK)
    if record:
        number = int(input("Correct Value:\t"))
        AppendColorFile(filepath,{
            'number': number,
            'r': color[0],
            'g': color[1],
            'b': color[2]
        })
    # logging.debug(f"top: {top}")
    # number = int(input("What is the actual Number:\t"))
    # if number != top:
    #     return number
    return top, color

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
        "r": math.floor(finalColor[0]),
        "g": math.floor(finalColor[1]),
        "b": math.floor(finalColor[2])
    }



# =======================================
# INPUT
# =======================================



def ClickMouse(x: int, y: int) -> None:
    """
    Clicks the mouse at a given location.
    
    Args:
        x: The x-coordinate of the mouse.
        y: The y-coordinate of the mouse.
    """

    mouse = MouseController()
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)

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

    keyboard = KeyController()
    if keyNum == 0:
        logging.info('== Pressed: UP ==')
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif keyNum == 1:
        logging.info('== Pressed: RIGHT ==')
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif keyNum == 2:
        logging.info('== Pressed: DOWN ==')
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif keyNum == 3:
        logging.info('== Pressed: LEFT ==')
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    else:
        raise ValueError