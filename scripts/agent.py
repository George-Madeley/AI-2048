"""
This script holds the agent class and functionality for the agent to solve the puzzle.
"""

from random import randint
from turtle import st
from state import GameState

import numpy as np


class Agent:
    def __init__(self, maxDepth: int) -> None:
        self.__gameState: GameState = None
        self.maxDepth = maxDepth

    def GetNextMove(self, tileNumberList):
        array = np.array(tileNumberList)
        self.__gameState = GameState(array, self.maxDepth)
        nextMove = self.FindBestMove()
        return nextMove

    def FindBestMove(self):
        """
        Search through the game states tree to find the best possible next move.
        
        Returns:
            The best next move.
        """
        # Find best score
        score = self.GetBestChildStateScore()
        # If best score is -1, there are no more possible moves.
        if score == -1:
            raise ValueError("Score was -1")

        # Find path to the best score
        path = self.FindPath(score, self.__gameState)

        # If path is None, an Error has occured in finding the best score
        if path is None:
            raise ValueError("Best Score calculated but could not be found.")

        # Find the next move to make to get to the best score.
        for move, child in enumerate(self.__gameState.children):
            if child is None: continue
            if child is path[1]:
                return move
        raise ValueError("Next move could not be found.")
        
    def GetBestChildStateScore(self) -> int:
        """
        Searches through the game state tree to find the leaf with the highest score.
        
        Returns:
            The highest Score.
        """

        bestScore = -1
        frontier = [self.__gameState]
        while frontier:
            state = frontier.pop(0)
            if state is None: continue
            if hasattr(state, 'children'):
                frontier.extend(state.children)
            else:
                if state.score >= bestScore:
                    bestScore = state.score
        return bestScore

    def FindPath(self, score: int, state: object) -> any:
        """
        Finds the path to the leaf with the given score.

        Args:
            score: The score to be found.
            state: The game state to search.

        Returns:
            The path to the goal state or None value.
        """

        if state is None: return None
        
        if hasattr(state, 'children'):
            for child in state.children:
                path = self.FindPath(score, state=child)
                if path != None:
                    return [state] + path
            return None
        else:
            if state.score == score:
                return [state]
            else:
                return None

