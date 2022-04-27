"""
This script holds the functionality to record data to the record files.
"""

import csv

def RecordToCSV(data: dict, filepath: str) -> bool:
    """
    Records data to a CSV file.
    
    Args:
        data: (dict) The data to be stored in the csv.
        filepath: (str) The file path to the csv file.
        
    Returns:
        True if the data was successfully stored to the CSV.
    """

    headers = ['id', 'test no.', 'score', 'highest value']
    try:
        with open(filepath, 'w') as output:
            outputDictWriter = csv.DictWriter(output, headers)
            outputDictWriter.writeheader()
            outputDictWriter.writerow(data)
        return True
    except ValueError:
        print("CSV File error occured.")
        return False