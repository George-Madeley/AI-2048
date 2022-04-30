"""
This script holds the agent class and functionality for the agent to solve the puzzle.
"""

from random import randint
from state import GameState

import numpy as np


class Agent:
    def __init__(self, maxDepth: int) -> None:
        self.__gameState: GameState = None
        self.maxDepth = maxDepth

    def GetNextMove(self, tileNumberList):
        array = np.array(tileNumberList)
        self.__gameState = GameState(array, self.maxDepth)

