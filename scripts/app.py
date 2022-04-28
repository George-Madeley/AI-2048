import sys
import time


from streamio import ReadConfigFile, ReadColorFile, RecordData
from agent import Agent
from interface import GetInformation, PressKey

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    # Load in the congif files
    configFilePath = GetSystemArgs()
    config = ReadConfigFile(configFilePath)
    colorDict = ReadColorFile(config['colors'])

    # Launch the web driver
    options = Options()
    options.add_argument('start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(config['url'])
        # Play the game
        PlayGame(config, colorDict)

def PlayGame(config: dict, colorDict: dict) -> None:
    """
    Loops over the game until the game is over.
    
    Args:
        config: The configuration dict.
        colorDict: The dict of all known colors.
    """
    # Define an instance of Agent
    agent = Agent()
    gameOver = False
    turnNumber = 0
    while not gameOver:
        # Read data from screen
        tileNumberList = GetInformation(config, colorDict)
        # Check if game over.
        if gameOver:
            break
        # Pass data to agent and get responce from agent
        nextMove = agent.GetNextMove(tileNumberList)
        # Enter response
        PressKey(nextMove)
        turnNumber += 1
        # Sleep
        time.sleep(config['turndelay'])
    RecordData({
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

if __name__ == "__main__":
    main()