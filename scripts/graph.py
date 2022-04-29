import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

def GetMarker(number: int) -> str:
    """
    Gets a marker based on the number entered.
    
    Args:
        number: The number marker

     Returns:
        A string of the marker.
    """

    if number == 0:
        return 'o'
    elif number == 2:
        return '*'
    elif number == 4:
        return 'v'
    elif number == 8:
        return 's'
    elif number == 16:
        return 'd'
    else:
        raise ValueError('Invalid number entered.')

def GetHexColor(r: int, g: int, b: int) -> str:
    """
    Gets the hexcode for the rgb color.
    
    Args:
        r: The red value.
        g: The green value.
        b: The blue value.
        
    Returns:
        The string of the color value.
    """

    r = hex(r)[2:]
    g = hex(g)[2:]
    b = hex(b)[2:]
    return "#" + r + g + b
    

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

filename = sys.argv[1]

alreadyPlotted = []

with open(filename) as colorCSV:
    colorDictReader = csv.DictReader(colorCSV, ['number', 'r', 'g', 'b'])
    for row in colorDictReader:
        if row['number'] == 'number': continue
        number = int(row['number'])
        r = int(row['r'])
        g = int(row['g'])
        b = int(row['b'])
        if [number, r, g, b] in alreadyPlotted : continue
        alreadyPlotted.append([number, r, g, b])
        marker = GetMarker(number)
        color = GetHexColor(r, g, b)
        ax.scatter(r, g, b, marker=marker, color=color)

ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')

plt.show()