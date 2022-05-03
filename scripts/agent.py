"""
This script holds the agent class and functionality for the agent to solve the puzzle.
"""

import math
from random import randint
from state import GameState

import numpy as np


class Agent:
    def __init__(self, maxDepth: int) -> None:
        self.__gameState: GameState = None
        self.maxDepth = maxDepth

    def GetNextMove(self, tileNumberList: list, moveToRemove: int = None) -> int:
        """
        Gets the best possible move.
        
        Args:
            tileNumberList: A list of the read tile values.
            moveToRemove: A number representing the move to remove.
            
        Returns:
            A number representing the next move to take.
        """

        array = np.array(tileNumberList)
        if moveToRemove is not None:
            self.__gameState.RemoveChild(moveToRemove)
        else:
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
        score = self.GetBestChildStateScore(smallest=True)
        # If best score is -1, there are no more possible moves.
        if score == -1 or score == math.inf:
            return -1

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
        
    def GetBestChildStateScore(self, smallest: bool = False) -> int:
        """
        Searches through the game state tree to find the leaf with the best score.
        
        Args:
            smallest: True if the impliementer wants to find the smallest value in the tree.

        Returns:
            The highest Score.
        """

        bestScore = math.inf if smallest else -1
        frontier = [self.__gameState]
        while frontier:
            state = frontier.pop(0)
            if state is None: continue
            if hasattr(state, 'children'):
                frontier.extend(state.children)
            else:
                if smallest:
                    if state.score <= bestScore:
                        bestScore = state.score
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

    def GetArrayOfNextMove(self, move: int) -> object:
        """
        Gets the next array of the provided move.
        
        Args:
            move: The move number.
            
        Returns:
            The array made from performing the given move.
        """

        return self.__gameState.children[move].array