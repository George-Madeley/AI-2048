"""
Author: George Madeley,
Date: 29/04/2022

Description:
    - Root file connecting all other scripts together.
    - Manages the agent.
    - Plays the game.
    - Calculates scores.
"""

from distutils.log import debug
import sys
import time
import logging

import numpy as np


from streamio import ReadConfigFile, ReadColorFile, RecordData
from agent import Agent
from interface import GetInformation, PressKey, ClickMouse, AppendColorFile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    # Load in the congif files
    configFilePath = GetSystemArgs()
    config = ReadConfigFile(configFilePath)
    colorList = ReadColorFile(config['colors'])

    # Launch the web driver
    options = Options()
    options.add_argument('start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(config['url'])
        # Play the game
        PlayGame(config, colorList)

def PlayGame(config: dict, colorList: list) -> None:
    """
    Loops over the game until the game is over.
    
    Args:
        config: The configuration dict.
        colorDict: The list of all known colors.
    """
    # Define an instance of Agent
    agent = Agent(config['maxdepth'])
    nextMove = 0
    turnNumber = 0

    # Use mouse to remove popup window
    time.sleep(1)
    mouseX = config["button1"]["x"]
    mouseY = config["button1"]["y"]
    ClickMouse(mouseX, mouseY)

    predictedArray = None

    while True: #nextMove >= 0:
        # Sleep
        time.sleep(config['turndelay'])
        # Read data from screen
        tileNumberList, tileColorList = GetInformation(config, colorList)
        # Compare prediected and read arrays
        tileNumberList = CompareStates(tileNumberList, predictedArray, tileColorList, colorList, config)
        # Pass data to agent and get responce from agent
        nextMove = agent.GetNextMove(tileNumberList)
        # Checks if game is over
        if nextMove < 0:
            break
        predictedArray = agent.GetArrayOfNextMove(nextMove)
        # Sleep
        time.sleep(config['turndelay'])
        # Enter response
        PressKey(nextMove)
        turnNumber += 1

    RecordData(config['recordfile'], {
        "score": CalculateScore(tileNumberList),
        "highest value": GetHighestTile(tileNumberList),
        "total moves": turnNumber
    })
    print("===== Game Over =====")

def CalculateScore(tileNumberList: list) -> int:
    """
    Sums up all the numbers on the board.
    
    Args:
        tileNumberList: a 2D-arry representing the game board.
        
    Returns:
        The sum of all numbers on the board.
    """

    total = 0
    for row in tileNumberList:
        for element in row:
            total += element
    return total

def GetHighestTile(tileNumberList: list) -> int:
    """
    Finds the highest number on the board.
    
    Args:
        tileNumberList: a 2D-arry representing the game board.
        
    Returns:
        The highest number on the board.
    """

    maxNum = 0
    for row in tileNumberList:
        for elemnet in row:
            if elemnet > maxNum:
                maxNum = elemnet
    return maxNum

def GetSystemArgs() -> str:
    """
    Gets the system arguments.
    
    Returns:
        The config file path.
    """

    if len(sys.argv) != 2:
        print(f"You have the incorrect number of arguments: {len(sys.argv)}")
        print(f"You need to have 2 arguments: the name of the python file and the config file.")
        raise ValueError("Incorrect number of input arguments.")
    else:
        return sys.argv[1]

def CompareStates(
    currentArray: np.ndarray,
    predictedArray: np.ndarray,
    tileColorList: list,
    colorList: list,
    config: dict) -> None:
    """
    Compares the two given arrays.
    
    Args:
        currentArray: The current read array.
        predictedArray: The AI predicted array.
        tileColorList: The list of read colors.
        colorList: The list of known colors.
    """

    if predictedArray is None: return currentArray

    logging.debug('Predicted Array:')
    print(predictedArray)
    logging.debug('Read Array:')
    print(np.array(currentArray))
    # if input("Does predicted match screen? [Y/n]\t").lower() == 'n':
    #     time.sleep(2)
    #     return currentArray
    # time.sleep(2)

    if CountTileSpawns(predictedArray, currentArray) > 1:
        logging.debug("The app believes two tiles have spawned at once. Please correct this.")
        needCorrecting = True
        while needCorrecting:
            x = int(input("X:\t")) - 1
            y = int(input("Y:\t")) - 1
            value = int(input("Value:\t"))
            currentArray[y][x] = value
            colorCode = tileColorList[y][x]
            AppendColorFile(config['colors'], {
                'number': value,
                'r': colorCode[0],
                'g': colorCode[1],
                'b': colorCode[2]
            })
            colorList.append((
                value,
                colorCode
            ))
            needCorrecting = input("Does the board need correcting? [Y/n]\t").lower() == 'y'
            time.sleep(3)

    height, width = predictedArray.shape
    for y in range(height):
        for x in range(width):
            if predictedArray[y][x] != currentArray[y][x]:
                if currentArray[y][x] <= 4 and predictedArray[y][x] == 0: continue
                colorCode = tileColorList[y][x]
                if not IsColorInColorList(colorCode, colorList):
                    AppendColorFile(config['colors'], {
                        'number': predictedArray[y][x],
                        'r': colorCode[0],
                        'g': colorCode[1],
                        'b': colorCode[2]
                    })
                    colorList.append((
                        predictedArray[y][x],
                        colorCode
                    ))
                currentArray[y][x] = predictedArray[y][x]
            else:
                if currentArray[y][x] <= 4 and predictedArray[y][x] == 0: continue
                colorCode = tileColorList[y][x]
                if not IsColorInColorList(colorCode, colorList):
                    AppendColorFile(config['colors'], {
                        'number': predictedArray[y][x],
                        'r': colorCode[0],
                        'g': colorCode[1],
                        'b': colorCode[2]
                    })
                    colorList.append((
                        predictedArray[y][x],
                        colorCode
                    ))
    logging.debug('Updated Array:')
    print(np.array(currentArray))
    return currentArray

def IsColorInColorList(color: np.ndarray, colorList: list) -> bool:
    """
    Checks if a given color is within the list of known colors.
    
    Args:
        color: The color to find.
        colorList: The list of known colors.
        
    Returns:
        True if color is in the list of known colors.
    """

    knownColors = [(row[1][0], row[1][1], row[1][2]) for row in colorList]
    color = (color[0], color[1], color[2])
    return color in knownColors

def CountTileSpawns(predictedArray: object, readArray: list) -> int:
    """
    Counts how many new tiles have been added to the board.
    
    Args:
        predictedArray: What the agent predicted the board would be like.
        readArray: The data read from the board.
    
    Returns:
        The number of new tiles.
    """

    height, width = predictedArray.shape
    count = 0
    for y in range(height):
        for x in range(width):
            if predictedArray[y][x] != readArray[y][x]:
                count += 1
    return count




logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('== Start of Program ==')

if __name__ == "__main__":
    main()