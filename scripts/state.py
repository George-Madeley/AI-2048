from itertools import combinations
import math
from turtle import width
import numpy as np

class GameState:
    """
    Class to represent a game state.
    """

    def __init__(self, array: np.array, maxDepth: int, depth: int = 0) -> None:
        self.array = array
        self.depth = depth
        self.maxDepth = maxDepth
        self.__score = None
        if depth < maxDepth:
            self.children = self.GenerateChildren()

    @property
    def score(self):
        """
        Score of the state.
        """

        if self.__score: return self.__score

        self.__score = self.CalculateScore()
        return self.__score

    @score.setter
    def score(self, value: int):
        self.__score = value

    def GenerateChildren(self):
        """
        Generates the four possible child states.

        Returns:
            A dict of all the possible child states.
        """

        return [
            self.GenerateUpChild(),
            self.GenerateRightChild(),
            self.GenerateDownChild(),
            self.GenerateLeftChild()
        ]

    def GenerateUpChild(self):
        """
        Generates the child state for if the agent moves upwards.
        
        Returns:
            The child state.
        """
        # Gets array size
        height, width = self.array.shape
        tempArray = self.array.copy()
        # Array where element is 1 if a combination just occured.
        combinationArray = np.zeros(self.array.shape)
        for y in range(height):
            for x in range(width):
                element = tempArray[y, x]
                # If element is 0, skip
                if not element: continue
                # creates temporary y value
                tempY = y
                # Performs a bubble sort
                while tempY - 1 >= 0:
                    # checks if there is a blank space above
                    blankSpaceAbove = tempArray[tempY - 1, x] == 0
                    # if there is a blank space above, move element into that space
                    if blankSpaceAbove:
                        tempArray[tempY - 1, x] = element
                        tempArray[tempY, x] = 0
                        tempY -= 1
                    # if there is no space, check if there is an element with the same value
                    else:
                        sameValueAbove = tempArray[tempY - 1, x] == element
                        canCombine = combinationArray[tempY - 1, x] == 0
                        # if there is an element with the same value, combine
                        if sameValueAbove and canCombine:
                            tempArray[tempY - 1, x] += element
                            tempArray[tempY, x] = 0
                            combinationArray[tempY - 1, x] = 1
                        break
        # Check if child array is the same as parent array
        if np.array_equal(tempArray, self.array):
            return None
        return GameState(tempArray, self.maxDepth, depth=self.depth + 1)

    def GenerateRightChild(self):
        """
        Generates the child state for if the agent moves to the right.
        
        Returns:
            The child state.
        """
        # Gets array size
        height, width = self.array.shape
        tempArray = self.array.copy()
        # Array where element is 1 if a combination just occured.
        combinationArray = np.zeros(self.array.shape)
        for x in reversed(range(width)):
            for y in range(height):
                element = tempArray[y, x]
                # If element is 0, skip
                if not element: continue
                # creates temporary y value
                tempX = x
                # Performs a bubble sort
                while tempX + 1 < width:
                    # checks if there is a blank space to ther right
                    blankSpaceRight = tempArray[y, tempX + 1] == 0
                    # if there is a blank space to the right, move element into that space
                    if blankSpaceRight:
                        tempArray[y, tempX + 1] = element
                        tempArray[y, tempX] = 0
                        tempX += 1
                    # if there is no space, check if there is an element with the same value
                    else:
                        sameValueRight = tempArray[y, tempX + 1] == element
                        canCombine = combinationArray[y, tempX + 1] == 0
                        # if there is an element with the same value, combine
                        if sameValueRight and canCombine:
                            tempArray[y, tempX + 1] += element
                            tempArray[y, tempX] = 0
                            combinationArray[y, tempX + 1] = 1
                        break
        # Check if child array is the same as parent array
        if np.array_equal(tempArray, self.array):
            return None
        return GameState(tempArray, self.maxDepth, depth=self.depth + 1)

    def GenerateDownChild(self):
        """
        Generates the child state for if the agent moves downwards.
        
        Returns:
            The child state.
        """
        # Gets array size
        height, width = self.array.shape
        tempArray = self.array.copy()
        # Array where element is 1 if a combination just occured.
        combinationArray = np.zeros(self.array.shape)
        for y in reversed(range(height)):
            for x in reversed(range(width)):
                element = tempArray[y, x]
                # If element is 0, skip
                if not element: continue
                # creates temporary y value
                tempY = y
                # Performs a bubble sort
                while tempY + 1 < height:
                    # checks if there is a blank space below
                    blankSpaceBelow = tempArray[tempY + 1, x] == 0
                    # if there is a blank space below, move element into that space
                    if blankSpaceBelow:
                        tempArray[tempY + 1, x] = element
                        tempArray[tempY, x] = 0
                        tempY += 1
                    # if there is no space, check if there is an element with the same value
                    else:
                        sameValueBelow = tempArray[tempY + 1, x] == element
                        canCombine = combinationArray[tempY + 1, x] == 0
                        # if there is an element with the same value, combine
                        if sameValueBelow and canCombine:
                            tempArray[tempY + 1, x] += element
                            tempArray[tempY, x] = 0
                            combinationArray[tempY + 1, x] = 1
                        break
        # Check if child array is the same as parent array
        if np.array_equal(tempArray, self.array):
            return None
        return GameState(tempArray, self.maxDepth, depth=self.depth + 1)

    def GenerateLeftChild(self):
        """
        Generates the child state for if the agent moves to the left.
        
        Returns:
            The child state.
        """
        # Gets array size
        height, width = self.array.shape
        tempArray = self.array.copy()
        # Array where element is 1 if a combination just occured.
        combinationArray = np.zeros(self.array.shape)
        for x in range(width):
            for y in reversed(range(height)):
                element = tempArray[y, x]
                # If element is 0, skip
                if not element: continue
                # creates temporary y value
                tempX = x
                # Performs a bubble sort
                while tempX - 1 >= 0:
                    # checks if there is a blank space to the left
                    blankSpaceLeft = tempArray[y, tempX - 1] == 0
                    # if there is a blank space to the left, move element into that space
                    if blankSpaceLeft:
                        tempArray[y, tempX - 1] = element
                        tempArray[y, tempX] = 0
                        tempX -= 1
                    # if there is no space, check if there is an element with the same value
                    else:
                        sameValueLeft = tempArray[y, tempX - 1] == element
                        canCombine = combinationArray[y, tempX - 1] == 0
                        # if there is an element with the same value, combine
                        if sameValueLeft and canCombine:
                            tempArray[y, tempX - 1] += element
                            tempArray[y, tempX] = 0
                            combinationArray[y, tempX - 1] = 1
                        break
        # Check if child array is the same as parent array
        if np.array_equal(tempArray, self.array):
            return None
        return GameState(tempArray, self.maxDepth, depth=self.depth + 1)

    def RemoveChild(self, index: int) -> None:
        """
        Removes a child from the list of children at the given index.
        
        Args:
            index: The index of the child to remove.
        """

        self.children[index] = None

    def CalculateScore(self) -> int:
        """
        Calculates the states score.
        
        Returns:
            The score.
        """

        scoresArray = self.DifferenceInLog2()
        return np.sum(scoresArray)

    def SumProductOfFourAdjacentTiles(self) -> np.array:
        """
        Scans through each tile and sums the products of its value and the values of neighboring tiles.
        
        Returns:
            np.array of the resulting values.
        """
        
        sizeY, sizeX = self.array.shape
        tempArray = np.zeros((sizeY, sizeX))
        boundY = range(sizeY)
        boundX = range(sizeX)
        for y in boundY:
            for x in boundX:
                total = 0
                if x - 1 in boundX:
                    total += self.array[y][x] * self.array[y][x - 1]
                if x + 1 in boundX:
                    total += self.array[y][x] * self.array[y][x + 1]
                if y - 1 in boundY:
                    total += self.array[y][x] * self.array[y - 1][x]
                if y + 1 in boundY:
                    total += self.array[y][x] * self.array[y + 1][x]
                tempArray[y][x] = total
        return tempArray

    def SumProductOfTwoAdjacentTiles(self) -> np.array:
        """
        Scans through each tile and sums the products of its value and the values of neighboring tiles.
        
        Returns:
            np.array of the resulting values.
        """
        
        sizeY, sizeX = self.array.shape
        tempArray = np.zeros((sizeY, sizeX))
        boundY = range(sizeY)
        boundX = range(sizeX)
        for y in boundY:
            for x in boundX:
                total = 0
                if x - 1 in boundX:
                    total += self.array[y][x] * self.array[y][x - 1]
                if y - 1 in boundY:
                    total += self.array[y][x] * self.array[y - 1][x]
                tempArray[y][x] = total
        return tempArray
    
    def SumProductOfFourAdjacentTilesWithBounds(self) -> np.array:
        """
        Scans through each tile and sums the products of its value and the values of
        neighboring tiles. If the pieces is next to the bounds, its multiplied by itself.
        
        Returns:
            np.array of the resulting values.
        """
        
        sizeY, sizeX = self.array.shape
        tempArray = np.zeros((sizeY, sizeX))
        boundY = range(sizeY)
        boundX = range(sizeX)
        for y in boundY:
            for x in boundX:
                total = 0
                if x - 1 in boundX:
                    total += self.array[y][x] * self.array[y][x - 1]
                else:
                    total += self.array[y][x] ** 2
                if x + 1 in boundX:
                    total += self.array[y][x] * self.array[y][x + 1]
                else:
                    total += self.array[y][x] ** 2
                if y - 1 in boundY:
                    total += self.array[y][x] * self.array[y - 1][x]
                else:
                    total += self.array[y][x] ** 2
                if y + 1 in boundY:
                    total += self.array[y][x] * self.array[y + 1][x]
                else:
                    total += self.array[y][x] ** 2
                tempArray[y][x] = total
        return tempArray

    def DifferenceInLog2(self) -> np.array:
        """
        Scans through each tile and sums the different of neighboring tiles log2 values.

        Returns:
            np.array of the resulting value.
        """

        sizeY, sizeX = self.array.shape
        tempArray = np.zeros((sizeY, sizeX))
        boundY = range(sizeY)
        boundX = range(sizeX)
        for y in boundY:
            for x in boundX:
                if self.array[y][x] == 0: continue
                total = 0
                if x - 1 in boundX and self.array[y][x - 1] != 0:
                    total += abs(math.log2(self.array[y][x]) - math.log2(self.array[y][x - 1]))
                if x + 1 in boundX and self.array[y][x + 1] != 0:
                    total += abs(math.log2(self.array[y][x]) - math.log2(self.array[y][x + 1]))
                if y - 1 in boundY and self.array[y - 1][x] != 0:
                    total += abs(math.log2(self.array[y][x]) - math.log2(self.array[y - 1][x]))
                if y + 1 in boundY and self.array[y + 1][x] != 0:
                    total += abs(math.log2(self.array[y][x]) - math.log2(self.array[y + 1][x]))
                tempArray[y][x] = total
        return tempArray

