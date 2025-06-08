import pandas as pd
import json

def parse_csv(file_path: str) -> pd.DataFrame:
    """
    Parses a CSV file and returns a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: The parsed DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error parsing CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
def parse_json(file_path: str) -> dict:
    """
    Parses a JSON file and returns its content as a dictionary.
    
    Args:
        file_path (str): The path to the JSON file.
        
    Returns:
        dict: The parsed JSON content.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error parsing JSON file: {e}")
        return {}  # Return an empty dictionary on error