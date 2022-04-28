"""
This script holds the functionality to record data to the record files.
"""

import csv
import json

def RecordData(data: dict, filepath: str) -> bool:
    """
    Records data to a CSV file.
    
    Args:
        data: (dict) The data to be stored in the csv.
        filepath: (str) The file path to the csv file.
        
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

def ReadColorFile(filepath: str) -> dict:
    """
    Reads the data from the provided color file.
    
    Args:
        filepath: The filepath to the color config file.
        
    Returns:
        A dict of the data in the color file.
    """

    colorDict = {}
    with open(filepath) as colorCSV:
        colorDictReader = csv.DictReader(colorCSV, ['number','r','g','b'])
        for row in colorDictReader:
            number = row['number']
            if number == 'number': continue
            colorDict[number] = {
                'r': int(row['r']),
                'g': int(row['g']),
                'b': int(row['b'])
            }
    return colorDict

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