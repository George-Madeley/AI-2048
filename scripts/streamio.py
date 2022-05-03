"""
Author: George Madeley,
Date: 29/04/2022

Description:
    - Reads data from the color.csv file and appsettings.json file.
    - Converts the read data into the correct format for the rest of the program.
    - Writes the test results to the correct files.
"""

import csv
import json
import numpy as np

def AppendColorFile(filepath: str, color: dict) -> None:
    """
    Appends a new color to the provided color file.
    
    Args:
        filepath: The filepath to the color config file.
        color: The color to appened.
    """

    with open(filepath, 'a', newline='') as colorCSV:
        colorDictWriter = csv.DictWriter(colorCSV, ['number','r','g','b'])
        colorDictWriter.writerow(color)

def CalculateCentroids(colorDict: dict) -> dict:
    """
    Calculates the centroid of each color.
    
    Args:
        The color dict from the read color file.
        
    Returns:
        A dict of all the color centroids.
    """

    totalDict = {}
    for row in colorDict:
        number = row['number']
        if number == 'number': continue
        if number not in totalDict.keys():
            totalDict[number] = {
                'r': int(row['r']),
                'g': int(row['g']),
                'b': int(row['b']),
                'count': 1
            }
        else:
            totalDict[number]['r'] += int(row['r'])
            totalDict[number]['g'] += int(row['g'])
            totalDict[number]['b'] += int(row['b'])
            totalDict[number]['count'] += 1
    centroidDict = {}
    for number, field in totalDict.items():
        centroidDict[number] = {
            'r': field['r'] / field['count'],
            'g': field['g'] / field['count'],
            'b': field['b'] / field['count']
        }
    return centroidDict

def ConvertToArray(oldList: list) -> list:
    """
    Converts the list of dicts to a list of tuples containing the key and the numpy array.
    
    Args:
        oldList: The old list of dicts.
        
    Returns:
        The list of tuples.
    """

    newList = []
    for dictionary in oldList:
        newList.append((
            dictionary['number'],
            list(dictionary.values())[1:]
        ))
    return newList

def EliminateDuplicates(oldList: list) -> list:
    """
    Eliminates any duplicate data from the list.
    
    Args:
        oldList: The list to elimate duplicate data from.
        
    Returns:
        A list with no duplicate data.
    """

    newList = []
    for row in oldList:
        if row in newList: continue
        if row['number'] == 'number': continue
        newList.append({
            'number': int(row['number']),
            'r': int(row['r']),
            'g': int(row['g']),
            'b': int(row['b'])
        })
    return newList

def ReadColorFile(filepath: str) -> list:
    """
    Reads the data from the provided color file.
    
    Args:
        filepath: The filepath to the color config file.
        
    Returns:
        A list of the data in the color file.
    """

    with open(filepath) as colorCSV:
        colorDictReader = csv.DictReader(colorCSV, ['number','r','g','b'])
        colorList = EliminateDuplicates(colorDictReader)
        colorArray = ConvertToArray(colorList)
    return colorArray

def ReadConfigFile(filepath: str) -> dict:
    """
    Reads the data from the provided config file.
    
    Args:
        filepath: The filepath to the config file.
        
    Returns:
        A dict of the data in the config file.
    """

    configDict = None
    with open(filepath) as configFile:
        configDict =  json.load(configFile)
    return configDict

def RecordData( filepath: str, data: dict) -> bool:
    """
    Records data to a CSV file.
    
    Args:
        filepath: (str) The file path to the csv file.
        data: (dict) The data to be stored in the csv.
        
    Returns:
        True if the data was successfully stored to the CSV.
    """

    headers = ['test no.', 'score', 'highest value', 'total moves']
    try:
        with open(filepath, 'w') as output:
            outputDictWriter = csv.DictWriter(output, headers)
            outputDictWriter.writeheader()
            outputDictWriter.writerow(data)
        return True
    except ValueError:
        print("CSV File error occured.")
        return False










